resource "digitalocean_kubernetes_cluster" "kubernetes-scavenger" {
  name   = "scavenger"
  region = "sfo3"
  # Grab the latest version slug from `doctl kubernetes options versions`
  version = "1.22.8-do.0"

  node_pool {
    name       = "worker-pool"
    size       = "s-2vcpu-2gb"
    node_count = 2
  }
}
