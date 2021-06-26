# Stocks::Orders::MarketOrder

A market order is a request to buy or sell a security at the currently available market price. The order to buy a security will be submitted on resource creation and the security will be sold (or the unfilled order cancelled) on resource deletion. Supported exchanges are AMEX, ARCA, BATS, NYSE, NASDAQ and NYSEARCA.

## Configuration

The type configuration should look like the following:

```
{
	"Credentials": {
		"Environment": "PAPER",
		"ApiKey": "YOURAPIKEY",
		"SecretKey": "YOURSECRETKEY"
	}
}
```

where `Environment` is either "PAPER" (recommended) or "LIVE".

## Docs

The docs can be found [here](https://github.com/iann0036/cfn-types/blob/master/stocks-orders-marketorder/docs/README.md).
