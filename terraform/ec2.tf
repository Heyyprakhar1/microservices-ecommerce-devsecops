resource "aws_vpc" "my" {
  cidr_block = var.aws_vpc_cidr
  tags = {
    Name = var.aws_vpc_name
  }
}
resource "aws_subnet" "my" {
    vpc_id            = aws_vpc.my.id
    cidr_block        = var.aws_subnet_cidr
    availability_zone = "eu-west-1a"
    tags = {
        Name = var.aws_subnet_name
    }
}
resource "aws_internet_gateway" "my" {
    vpc_id = aws_vpc.my.id
}
resource "aws_key_pair" "my" {
    key_name   = "online-shop-key"
    public_key = file(var.aws_key_pair_public_key)
    tags = {
        Name = var.aws_key_pair_public_key
    }
}
resource "aws_security_group" "my" {
    name        = var.aws_security_group_name
    description = "Security group for online shop EC2 instance"
    vpc_id      = aws_vpc.my.id
    ingress {
        from_port   = 80
        to_port     = 80
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
    ingress {
        from_port   = 22
        to_port     = 22
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
    egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}
resource "aws_instance" "my" {
    ami           = data.aws_ami.amazon_linux.id
    count         = length(var.aws_instance_types)
    instance_type = var.aws_instance_types[count.index]
    vpc_security_group_ids = [aws_security_group.my.id]
    tags = {
        Name = "${var.aws_instance_name}-${count.index}"
    }
}
resource "aws_ami_from_instance" "my" {
  count              = length(aws_instance.my)
  name               = "online-shop-ami-${count.index}"
  source_instance_id = aws_instance.my[count.index].id
}