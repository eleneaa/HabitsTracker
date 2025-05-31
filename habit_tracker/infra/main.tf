terraform {
  required_providers {
    yandex = {
      source  = "yandex-cloud/yandex"
      version = "~> 0.80"
    }
  }
}

provider "yandex" {
  token     = var.yc_token
  cloud_id  = var.cloud_id
  folder_id = var.folder_id
  zone      = var.zone
}

# VPC и подсеть
resource "yandex_vpc_network" "default" {
  name = "django-network"
}

resource "yandex_vpc_subnet" "default" {
  name           = "django-subnet"
  zone           = var.zone
  network_id     = yandex_vpc_network.default.id
  v4_cidr_blocks = ["10.0.0.0/24"]
}

# Object Storage bucket
resource "yandex_storage_bucket" "media" {
  bucket     = var.bucket_name
  access_key = var.s3_access_key
  secret_key = var.s3_secret_key
  max_size   = 5368709120
}

# PostgreSQL Managed Cluster
resource "yandex_mdb_postgresql_cluster" "pg_cluster" {
  name        = "pg-django"
  environment = "PRESTABLE"
  network_id  = yandex_vpc_network.default.id

  config {
    version = "14"
    resources {
      resource_preset_id = "s2.micro"
      disk_size          = 10
      disk_type_id       = "network-ssd"
    }
  }

  host {
    zone           = var.zone
    subnet_id      = yandex_vpc_subnet.default.id
    assign_public_ip = true
  }
}

resource "yandex_mdb_postgresql_user" "user" {
  cluster_id = yandex_mdb_postgresql_cluster.pg_cluster.id
  name       = var.db_user
  password   = var.db_password #
}

resource "yandex_mdb_postgresql_database" "db" {
  cluster_id = yandex_mdb_postgresql_cluster.pg_cluster.id
  name       = var.db_name
  owner      = yandex_mdb_postgresql_user.user.name

  depends_on = [yandex_mdb_postgresql_user.user]
}


# VM для Django
data "yandex_compute_image" "ubuntu" {
  family = "ubuntu-2204-lts"
}

resource "yandex_compute_instance" "django" {
  name        = "django-vm"
  zone        = var.zone
  platform_id = "standard-v1"

  resources {
    cores  = 2
    memory = 2
  }

  boot_disk {
    initialize_params {
      image_id = data.yandex_compute_image.ubuntu.id
      size     = 10
    }
  }

  network_interface {
    subnet_id          = yandex_vpc_subnet.default.id
    nat                = true
  }

metadata = {
  ssh-keys = "ubuntu:${file("~/.ssh/id_rsa.pub")}"
  user-data = <<-EOF
    #cloud-config
    package_update: true
    packages:
      - docker.io
    runcmd:
      - systemctl start docker
      - docker login cr.yandex --username oauth --password y0__xD13u79AxjB3RMgs9PgxxIXhaeU827dqObuYt4jDWFsgwpVRw
      - docker pull cr.yandex/crpdg9p1l3qf6a0i2h83/habit_tracker:latest
      - docker run -d -p 80:8000 -e DB_HOST=${yandex_mdb_postgresql_cluster.pg_cluster.host[0].fqdn} -e DB_NAME=${var.db_name} -e DB_USER=${var.db_user} -e DB_PASSWORD=${var.db_password} -e YC_BUCKET_NAME=${yandex_storage_bucket.media.bucket} cr.yandex/crpdg9p1l3qf6a0i2h83/habit_tracker:latest
  EOF
}

}

# Load Balancer Target Group
resource "yandex_lb_target_group" "tg" {
  name = "django-tg"

  target {
    subnet_id = yandex_vpc_subnet.default.id
    address   = yandex_compute_instance.django.network_interface[0].ip_address
  }
}

# Network Load Balancer
resource "yandex_lb_network_load_balancer" "lb" {
  name = "django-lb"

  listener {
    name = "http"
    port = 80

    external_address_spec {
      ip_version = "ipv4"
    }
  }

  attached_target_group {
    target_group_id = yandex_lb_target_group.tg.id

    healthcheck {
      name = "http"
      http_options {
        port = 80
        path = "/health/"
      }
    }
  }
}
