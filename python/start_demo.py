import aws_madzumo

def main():
    samplex = aws_madzumo.AWSconfig()
    # samplex.create_ec2_instance()
    samplex.delete_ec2_instance()
if __name__ == "__main__":
    main()