output "instance_details" {
    description = "All EC2 instance details grouped by name"
    value = {
        for key, instance in aws_instance.my : key => {
            id         = instance.id
            public_ip  = instance.public_ip
            private_ip = instance.private_ip
            public_dns = instance.public_dns
        }
    }
}