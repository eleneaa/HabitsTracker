variable "yc_token" {}
variable "cloud_id" {}
variable "folder_id" {}
variable "zone" {
  default = "ru-central1-a"
}

variable "bucket_name" {}
variable "s3_access_key" {}
variable "s3_secret_key" {}

variable "db_name" {
  default = "habits"
}
variable "db_user" {
  default = "habits_user"
}
variable "db_password" {}
