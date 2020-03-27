# reflex-aws-s3-bucket-policy-public-access
Detect when a bucket has a Bucket Policy that grant public access.

## Usage
To use this rule either add it to your `reflex.yaml` configuration file:  
```
rules:
  - reflex-aws-s3-bucket-policy-public-access:
      version: latest
```

or add it directly to your Terraform:  
```
...

module "reflex-aws-s3-bucket-policy-public-access" {
  source           = "github.com/cloudmitigator/reflex-aws-s3-bucket-policy-public-access"
}

...
```

## License
This Reflex rule is made available under the MPL 2.0 license. For more information view the [LICENSE](https://github.com/cloudmitigator/reflex-aws-s3-bucket-policy-public-access/blob/master/LICENSE)
