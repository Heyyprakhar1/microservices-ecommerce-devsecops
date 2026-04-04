output "aws_instance_my_public_ip" {
    description = "The public IP address of the EC2 instance"
    value       = aws_instance.my[*].public_ip
}
output "aws_instance_my_public_dns" {
    description = "The public DNS name of the EC2 instance"
    value       = aws_instance.my[*].public_dns
}
output "aws_instance_my_id" {
    description = "The ID of the EC2 instance"
    value       = aws_instance.my[*].id
}
output "aws_instance_my_ami" {
    description = "The AMI ID of the EC2 instance"
    value       = aws_instance.my[*].ami

}
output "aws_instance_my_instance_type" {
    description = "The instance type of the EC2 instance"
    value       = aws_instance.my[*].instance_type
}