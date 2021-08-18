from django.template.defaulttags import register

# Enables access to dictionaries elements inside templates  ({{ dict|get_item:item.item}})
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

# Return a dictionary with the highest bid for each listing  -- {'product': 'bid'}
def highBid(bids):
    highestBids = {}
    # Populate dictionary with only the highest bid for each listing
    for bid in bids:
        if bid.product.id not in highestBids:
            highestBids[bid.product.id] = bid.bid
        elif bid.product.id in highestBids and bid.bid > highestBids[bid.product.id]:
            highestBids.update({bid.product.id: bid.bid})
        else:
            continue
    return highestBids
