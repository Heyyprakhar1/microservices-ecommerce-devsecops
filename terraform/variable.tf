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
variable "aws_key_pair_private_key" {
    description = "The private key for the AWS key pair"
    type        = string
    default     = "online-shop-key.pem"
}
variable "aws_security_group_name" {
    description = "The name of the security group"
    type        = string
    default     = "online-shop-sg"
}
variable "aws_instance_types" {
    description = "List of instance types"
    type        = list(string)
    default     = ["t2.micro", "t2.small", "t2.medium"]
}
variable "aws_instance_name" {
    description = "The name of the EC2 instance"
    type        = string
    default     = "online-shop-instance"
}
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*"]
  }
}