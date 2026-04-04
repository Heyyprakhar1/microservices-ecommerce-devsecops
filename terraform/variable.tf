variable "aws_region" {
  description = "The AWS region to deploy resources in"
  type        = string
  default     = "eu-west-1"
}
variable "aws_vpc_cidr" {
    description = "The CIDR block for the VPC"
    type        = string
    default     = "10.0.0.0/16"
}
variable "aws_vpc_name" {
    description = "The name of the VPC"
    type        = string
    default     = "online-shop-vpc"
}
variable "aws_subnet_cidr" {
    description = "The CIDR block for the subnet"
    type        = string
    default     = "10.0.0.0/24"
}
variable "aws_subnet_name" {
    description = "The name of the subnet"
    type        = string
    default     = "online-shop-subnet"
}
variable "aws_key_pair_public_key" {
    description = "The public key for the AWS key pair"
    type        = string
    default     = "online-shop-key.pub"
}
variable "aws_security_group_name" {
    description = "The name of the security group"
    type        = string
    default     = "online-shop-sg"
}
variable "instances" {
    description = "Map of instance names to their AmI IDs and SSH users & OS family"
    type = map(object({
        ami_id   = string
        ssh_user = string
        os_family = string
        instance_type = string
    }))
    default = {
        "master-ubuntu" = {
            ami_id   = "ami-0324bce2436ce02b2"
            ssh_user = "ubuntu"
            os_family = "ubuntu"
            instance_type  = "t2.micro"
        },
        "worker-linux" = {
            ami_id   = "ami-0762bad84218d1ffa"
            ssh_user = "ec2-user"
            os_family = "linux"
            instance_type  = "t2.small"
        },
        "worker-ubuntu" = {
            ami_id   = "ami-0324bce2436ce02b2"
            ssh_user = "ubuntu"
            os_family = "ubuntu"
            instance_type  = "t2.medium"
        }
    }
}