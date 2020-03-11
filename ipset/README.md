# Ipset app notes

I tried cleaning ipsets periodically
via `django-q` schedules,
and `django-q` is great,
but it spawns five processes
and eats at least 15% of the memory
of a $5 droplet,
so a management command is
more economical.

This,
and consideration of the need for efficiency
in the blacklist features,
makes me think that this whole project
should be re-written in golang.
Only the whitelist is implemented here
so I can move forward
without doing so
and use the existing firewall
to implement port knocking
in projects that depend on the stack.


## App

The ipset app
provides a simple HTTP API
to let other processes on localhost:

- Add addresses temporarily
  to the admin whitelist ipset.
- Add addresses temporarily or permanently
  to global blacklist ipset (TODO).

The app assumes
the existence of IPv4 and IPv6
whitelist and blacklist ipsets on a host,
that firewall rules
allow access to the host's SSH port
only from addresses in the whitelist ipsets,
and that firewall rules
block access to all transports and ports
from addresses in the blacklist ipsets
before the firewall tracks connection state.

The app also assumes the existence
of statically configured ipset membership
that it knows nothing about.
In other words,
it takes into account
that a separate process has preloaded ipsets
with addresses that should be permanent members
of whitelist and blacklist ipsets
and that the app shouldn't remove them.

Firewall init methods
run in the ipset app config `ready` method
when the app is started as an ASGI application.

Firewall clean methods
run in a management command.


## API endpoints

### Admin whitelist POST endpoint

**Keys and values**

The admin whitelist POST endpoint
accepts a single mandatory `address` key,
and the value is the IPv4 or IPv6 address
to add to the whitelist.

**Database and view**

The project database stores unique WhitelistAddress records.

When the POST endpoint receives a request,
it creates an address record if one doesn't already exist
or updates the last-access time
when a record for the address already exists.

To avoid removing statically configured addresses
from ipsets the app doesn't know about,
when a record for a POSTed address
doesn't yet exist,
the view tests the underlying ipset for the address
before adding a new whitelist record,
and if the address is already a member of the whitelist ipset,
the view ignores the request.

**Init**

Init deletes all whitelist records
from the app database on project start,
but doesn't remove addresses
from underlying ipsets.

**Clean**

Clean queries all expired records,
removes their addresses from underlying ipsets
and deletes the expired records.

Both the project and ipset service
should be restarted
after changing static ipset config
so existing records are cleared
and periodic ipset cleaning doesn't remove
statically whitelisted addresses.


### Global blacklist POST endpoint

Not implemented.

**Keys and values**

The global blacklist POST endpoint
accepts `address`, `timeout`, `severity` and `reason` keys.
Address values are IPv4 or IPv6 addresses,
severity values are integers,
timeout is a number of seconds a blacklist event should be valid,
and reason values are slugs.
Address and severity are mandatory,
and timeout and reason are optional.
Addresses are banned permanently
when the timeout key is not present.

**Database**

The project database stores
BlacklistAddress and BlacklistEvent records,
and BlacklistEvent records contain a foreign key reference
to BlacklistAddresses
to allows event records to be managed
by the BlacklistAddress object manager.

**View**

When the POST endpoint receives an event,
the view adds address and event records as necessary
and calculates the total severity
of all event records for the POSTed address.
When the severity total exceeds the ban threshold,
the view adds the address to the correct IPv4/IPv6 blacklist ipset.

For efficiency,
the view doesn't test
that POSTed addresses
are already members of a blacklist ipset
before adding records.
This means that if the API receives requests
to blacklist addresses already in the
statically configured blacklist set membership,
they might be removed from
the blacklist ipset when records expire.
If the firewall is blocking requests
from blacklisted addresses globally
before the firewall tracks connection state,
this shouldn't be an issue.
I hope.

**Init**

Blacklist init
removes address and event records from the project database
based on record timeout
but doesn't remove addresses from blacklist ipsets.

For remaining address records,
init tests the underlying ipset
and removes address and event records if it exists.
This avoids later removal
of the statically configured address from the ipset
by blacklist clean.

For all remaining address records,
init checks the accumulated severity
of events in blacklisted address' remaining records,
and if the total severity
is higher than the ban threshold,
it adds the address to the blacklist ipset.

The firewall API should not service requests
until init is complete.

**Clean**

Run blacklist clean periodically after project start
to remove records and addresses from blacklist ipsets
based on record age and timeout.

After removing expired records,
clean checks the accumulated severity
of events in blacklisted address' remaining records,
and if the total severity
is lower than the ban threshold,
removes the address from the blacklist ipset.

Clean doesn't remove records or addresses
for permanently banned addresses.

**Permanent bans**

When the API receives a blacklist event
with no timeout key or value,
or when the total severity of all blacklist events for an address
surpasses the permanent ban threshold,
the view marks the address record as permanently banned
and immediately adds it to the blacklist ipset.


### Global blacklist DELETE endpoint

TODO Is this a good idea?

The blacklist DELETE endpoint
accepts a single `address` key
and the value is the IPv4 or IPv6 address
to remove from the blacklist.

To avoid removing addresses
from static, permanently configured
blacklist addresses,
the request is ignored
if the address to remove
is not in the project database blacklist table.
