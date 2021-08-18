# splunk-addon-linode

The Linode Add-on for Splunk collects account events from Linode. 

## Usage

To install the app onto a Splunk instance, follow the steps outlined in the [installation section](#installation).

Linode accounts can be can be configured in the `Configuration` tab of the Add-on. A read-only Linode API token is required when configuring an account. See the official [Linode API Documentation](https://www.linode.com/docs/guides/getting-started-with-the-linode-api/#get-an-access-token) for more details on generating an API token.

Inputs are configured through the `Inputs` tab of the Add-on. Each input can have a specified index, Linode account, poll interval, and start date.  After an input is created, it will automatically begin polling Linode's API on the user-specified interval.

## Currently Supported Inputs

Name | Description
--- | ---
Account Events|Collect events from `/account/events`
Account Invoices|Collect invoices from `/account/invoices`
Account Logins|Collect logins from `/account/logins`
Account Notifications|Collect notifications from `/account/notifications`
Account Payments|Collect payments from `/account/payments`
Account Service Transfers|Collect service transfers from `/account/service-transfers`

## Installation

### Splunkbase

TODO

### Manual

The Splunk `.tgz` app file can be generated with the following command:

```shell
make build
```

In Splunk Enterprise, navigate to `manager/appinstall/_upload` and upload the generated `.tgz` file. Restart Splunk if prompted to do so, and the Add-on should be visible under the `Apps` drop-down.

## Contribution Guidelines

Want to improve splunk-addon-linode? Please start [here](CONTRIBUTING.md).