resource "digitalocean_project" "scavenger" {
  name        = "scavenger"
  description = "Resources for the Scavenger site."
  purpose     = "Web Site"
  environment = "Development"

  resources   = [digitalocean_database_cluster.postgres-scavenger.urn]
}

