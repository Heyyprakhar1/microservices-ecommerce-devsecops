resource "aws_vpc" "my" {
  cidr_block = var.aws_vpc_cidr
  tags = {
    Name = var.aws_vpc_name
  }
}
resource "aws_subnet" "my" {
    vpc_id            = aws_vpc.my.id
    cidr_block        = var.aws_subnet_cidr
    map_public_ip_on_launch = true
    tags = {
        Name = var.aws_subnet_name
    }
}
resource "aws_internet_gateway" "my" {
    vpc_id = aws_vpc.my.id
}
resource "aws_route_table" "my" {
    vpc_id = aws_vpc.my.id
    route {
        cidr_block = "0.0.0.0/0"
        gateway_id = aws_internet_gateway.my.id
    }
}
resource "aws_route_table_association" "my" {
    subnet_id      = aws_subnet.my.id
    route_table_id = aws_route_table.my.id
}
resource "aws_key_pair" "my" {
    key_name   = "online-shop-key"
    public_key = file(var.aws_key_pair_public_key)
    tags = {
        Name = "online-shop-key"
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
    for_each      = var.instances
    ami           = each.value.ami_id
    key_name      = aws_key_pair.my.key_name
    subnet_id     = aws_subnet.my.id
    vpc_security_group_ids = [aws_security_group.my.id]
    instance_type = each.value.instance_type
    root_block_device {
        volume_size = 10
        volume_type = "gp3"
    }
    tags = {
        Name = each.key
        OsFamily = each.value.os_family
    }
}