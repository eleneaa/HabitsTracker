output "bucket_url" {
  value = "https://${var.bucket_name}.storage.yandexcloud.net"
}

output "postgres_host" {
  value = yandex_mdb_postgresql_cluster.pg_cluster.host[0].fqdn
}

output "django_vm_ip" {
  value = yandex_compute_instance.django.network_interface.0.nat_ip_address
}

output "load_balancer_ip" {
  value = tolist(tolist(yandex_lb_network_load_balancer.lb.listener)[0].external_address_spec)[0].address
}

output "pg_cluster_host0" {
  value = yandex_mdb_postgresql_cluster.pg_cluster.host[0]
}


