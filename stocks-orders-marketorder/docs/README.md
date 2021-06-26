# Stocks::Orders::MarketOrder

A market order is a request to buy or sell a security at the currently available market price. The order to buy a security will be submitted on resource creation and the security will be sold (or the unfilled order cancelled) on resource deletion. Supported exchanges are AMEX, ARCA, BATS, NYSE, NASDAQ and NYSEARCA.

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "Type" : "Stocks::Orders::MarketOrder",
    "Properties" : {
        "<a href="#quantity" title="Quantity">Quantity</a>" : <i>Double</i>,
        "<a href="#symbol" title="Symbol">Symbol</a>" : <i>String</i>,
        "<a href="#notes" title="Notes">Notes</a>" : <i>String</i>,
    }
}
</pre>

### YAML

<pre>
Type: Stocks::Orders::MarketOrder
Properties:
    <a href="#quantity" title="Quantity">Quantity</a>: <i>Double</i>
    <a href="#symbol" title="Symbol">Symbol</a>: <i>String</i>
    <a href="#notes" title="Notes">Notes</a>: <i>String</i>
</pre>

## Properties

#### Quantity

The number of shares to buy.

_Required_: Yes

_Type_: Double

_Update requires_: [Replacement](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement)

#### Symbol

The stock symbol to buy.

_Required_: Yes

_Type_: String

_Update requires_: [Replacement](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement)

#### Notes

A fields for notes about the order. This field may also be used to force a resource update in order to retrieve the latest market value of the position.

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

## Return Values

### Ref

When you pass the logical ID of this resource to the intrinsic `Ref` function, Ref returns the Id.

### Fn::GetAtt

The `Fn::GetAtt` intrinsic function returns a value for a specified attribute of this type. The following are the available attributes and sample return values.

For more information about using the `Fn::GetAtt` intrinsic function, see [Fn::GetAtt](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html).

#### Id

A unique identifier for the order.

#### FilledQuantity

The total quantity filled.

#### FilledValue

The total notional value the order filled at.

#### CurrentValue

The latest trade price (quote) for the filled quantity.

#### FilledAt

The timestamp when the order was filled.

