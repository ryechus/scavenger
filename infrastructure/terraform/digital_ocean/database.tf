resource "digitalocean_database_cluster" "postgres-scavenger" {
  name       = "scavenger-postgres-cluster"
  engine     = "pg"
  version    = "14"
  size       = "db-s-1vcpu-1gb"
  region     = "sfo3"
  node_count = 1
}

resource "digitalocean_database_db" "database-scavenger-dev" {
  cluster_id = digitalocean_database_cluster.postgres-scavenger.id
  name       = "scavenger-dev"
}

resource "digitalocean_database_user" "database-user-scavenger" {
  cluster_id = digitalocean_database_cluster.postgres-scavenger.id
  name       = "scavenger"
}
