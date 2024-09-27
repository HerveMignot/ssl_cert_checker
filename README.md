# https-certificate-expiry-checker as a Function

This code is an adaptation from https://github.com/codebox/https-certificate-expiry-checker.

It can now be used as a Cloud Function for probing endpoints through website monitoring systems.

For example, it can be used with Montastic (https://montastic.com) to monitor the expiry of SSL/TLS certificates for a list of endpoints, in addition to the standard status checks that Montastic provides. This can be useful for ensuring that your website is always accessible over HTTPS, and that your certificates are not about to expire.


## Deploying as a Google Cloud Function

Use the `deploy.sh` script to deploye the function to GCP.

```bash
./deploy.sh your_project_id your_region
```

As a result, the URL to trigger the function should be displayed if deployment goes fine:
```
url: https://europe-west1-my-gcp-project.cloudfunctions.net/ssl-cert-checher
```

For more reference about deploying a Google Cloud Function, see: https://cloud.google.com/functions/docs/deploy


### Requirements

1. Install the Google Cloud SDK (https://cloud.google.com/sdk/docs/install) and authenticate with your Google Cloud account (https://cloud.google.com/sdk/docs/authorizing).
2. Create or choose a project on Google Cloud Platform (https://console.cloud.google.com/projectcreate) and enable the Cloud Functions API (https://console.cloud.google.com/apis/library/cloudfunctions.googleapis.com) on this project.
3. Make sure you have authenticated with an account having the Cloud Functions Developer IAM role (or equivalent) (https://cloud.google.com/functions/docs/reference/iam/roles#cloudfunctions.developer).


## Using the Cloud Function

It can easily be used by calling the URL of the Cloud Function with the `endpoint` parameter and optionally `warn` parameter. The `endpoint` parameter is a domain name to check. The `warn` parameter is the number of days before expiry that a warning should be issued. If the `warn` parameter is not provided, the default value of 7 days is used.

```bash
curl "https://europe-west1-my-gcp-project.cloudfunctions.net/ssl-cert-checher?endpoint=www.equancy.com&warn=30"
```

A POST query can also be used with a JSON body containing the `endpoint` and `warn` parameters. For example, using `curl`:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"endpoint": "www.equancy.com", "warn": 30}' "https://europe-west1-my-gcp-project.cloudfunctions.net/ssl-cert-checher"
```

### Parameters

* `endpoint` (required): The domain name to check. For example, `www.equancy.com`.
* `warn` (optional): The number of days before expiry that a warning should be issued. If not provided, the default value of 7 days is used.

## Appendix

### Original documentation from https-certificate-expiry-checker

This is a Python script for checking the expiry dates of website TLS/SSL certificates, used for creating secure HTTPS connections.

To use the script simply run it from the command line, along with a list of the domain names you wish to check. For example:

    > python check-certificates.py codebox.net www.codebox.net api.codebox.net oldtime.radio c0debox.net
    
    Checking 5 endpoints...
    codebox.net     OK    expires in 48 days
    www.codebox.net OK    expires in 48 days
    api.codebox.net OK    expires in 48 days
    oldtime.radio   WARN  expires in 6 days 21 hours 13 minutes
    c0debox.net     ERROR [Errno 8] nodename nor servname provided, or not known
 
The script will list the status of each domain's certificate, displaying '`OK`' if the certificate was retrieved and is not expiring soon, '`WARN`' if the certificate's expiry date is getting close, or '`ERROR`' if the certificate has already expired, or if there is some other problem such as the host could not be found, or no certificate could be retrieved.

By default '`WARN`' will be displayed if there are less than 7 days until a certificate expires, but this interval can be changed by altering the value of the [WARN_IF_DAYS_LESS_THAN](https://github.com/codebox/https-certificate-expiry-checker/blob/main/check-certificates.py#L13) variable.
 
If any of the domains are using a non-standard port for HTTPS then this should be specified using the usual notation of `host:port`, for example:

    > python check-certificates.py test.codebox.net:8443

The script returns an exit code indicating whether the checks passed or not, making it easier to take appropriate action in a shell script (for example, send a email if the checks fail):

| Condition | Exit Code |
|-----------|-----------|
| Everything is fine, none of the certificates are expiring soon | 0 |
| At least one certificate is expiring soon | 1 |
| At least one certificate has expired, is invalid, or could not be retrieved | 2 |
| Both of the previous conditions occurred | 3 |
| No domain list was provided when running the script | 9 |
 
Certificate checks are performed in parallel, making the process of checking multiple domains much quicker. The number of concurrent checks that will be performed is determined by the value of the [WORKER_THREAD_COUNT](https://github.com/codebox/https-certificate-expiry-checker/blob/main/check-certificates.py#L11) variable.