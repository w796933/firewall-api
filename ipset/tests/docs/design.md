# Design notes

The app provides:

A JSON interface
to add and remove addresses from underlying ipsets
using a Python wrapper around the ipset command line tool.

A management script to clear expired entries,

A maintenance function that
syncs the contents of underlying ipsets
with project settings
and entries in the project database.

The maintenance function runs
when the ipset app is ready (on project start).

## Ipsets

Underlying ipsets must already exist.
The app does not create or destroy them.
This should be done using the same
tooling that configures iptables firewall rules
for the host.

## IPv4 and IPv6 ipsets

The project manages
both IPv4 or IPv6 addresses
in the API and project settings,
but ipsets can contain addresses
only for a specific IP protocol,
so the project acts as a layer
between users and
the IPv4- and IPv6-specific ipsets.

This means that for each ipset listed in project settings,
two underlying ipsets must exist,
one that appends a 4 to the configured ipset name
(for IPv4 addresses)
and one that appends a 6
(for IPv6 addresses).

## Project settings

The app reads the IPSETS dict
from project settings.

Each key in the dict
corresponds to two underlying ipsets,
one for IPv4 addresses,
and one for IPv6.

IPv4- and IPv6-specific ipsets
must be pre-configured on the host
for each set listed in project settings.
The project does not create or destroy
underlying ipsets.

The dict maps ipset names
to lists of management addresses
that should NOT be removed
from underlying ipsets.

Ipset names in project settings
should be the raw name,
not the IPv4- or IPv6-specific
name of the underlying ipsets,
and settings' management address list
can contain both IPv4 and IPv6 addresses.

## Models

An Entry has a unique ID,
an IPv4 or IPv6 address,
and a set of Sets the Entry is in.

A Set has a name and a set of Entries.

Entries aren't quite the same
as iptables entries.
They're a unique ID and an address,
and Sets can contain many Entries with the same IP
but with different entry IDs.

Addresses remain in the underlying ipset
for as long as there's an Entry in the Set
with the given address.

Once the last Entry with a particular address
is removed from a Set,
the address is removed from the underlying ipset.

Entry IDs are up to 100 character strings,
and addresses are valid IPv4 or IPv6 addresses.

## API endpoints

Both endpoints take a unique entry ID as JSON data
in the body of PUT and DELETE methods.

The API provides ORM-based input validation,
but no authentication/authorization,
and no CSRF protection.

### /ipset/entry/ PUT

Takes entry ID and IPv4 or IPv6 address as data.

Creates a new entry with the supplied address
if the entry ID doesn't already exist,
or updates the address of an existing entry
if it does.

If the entry ID already exists,
update the expires field.

Raises 400 if the supplied address
can't be validated as either IPv4 or IPv6.

Entry ID is a string of up to 100 characters.

### /ipset/entry/ DELETE

Takes an entry ID as data.

Purges the entry
from all sets it's a member of
and deletes the entry from the project database.

Raises 404 if the entry
is missing from the project database.

### /ipset/set/ PUT

Takes entry ID and set name as data.

Adds the entry to a single set
and updates the expires field.

Raises 404 if the entry
is missing from the project database,
or 400 if the set is missing.

### /ipset/set/ DELETE

Takes entry ID and set name as data.

Purges an existing entry from a single set.

Raises 404 if the entry
is missing from the project database,
or 400 if the set is missing.

## Using the API

The process of creating an entry
and adding it to a set
is to PUT an entry ID and an address to /ipset/entry/,
then PUT the entry ID and a set to /ipset/set/.

It's entirely up to the API user
to select entry IDs,
so name collisions are possible.

The PUT and DELETE methods of /ipset/set/
allow configuration of only a single set per request.

## Deployment

The project is a layer
over the ipset command line utility.
The ipset command manages in-kernel data,
so it must run as root,
and so this project must run as root as well.

So to deploy somewhat safely,
the project should be cloned
into a directory read/writeable only by root,
and should be accessible
only on a localhost address and port.
I like to accomplish this
using Gunicorn and nginx.

## Iptables

Iptables should make use of sets somehow,
either to allow access to certain ports,
or to drop all traffic,
from the addresses in a set's entries,

## On ready sync

The app syncs ipset entries
when the ipset app is ready
on project start.

## Cleaning up old entries

Entries have expires fields,
and the `clearentries` management script
removes expired entries from sets
and deletes them from the database
if the current time is later than
what's in the expires field.

The script should be called periodically
to clear expired entries from the system.

Removing entries like this
creates complications for firewall users
when they try to update an entry
that has been removed by timout,
so entry DELETE and set PUT and DELETE
return 404 if the entry is missing,
but return 400 if the set doesn't exist.

## Puptel common app

The puptel project provides
a Django app with modules
that works with the firewall
to manage IP addresses.

The common app adds firewall entry info to session data
and adds users to the admin set
based on login and session delete signals.

It also supplies middleware that inspects entry session data
and current IP address
and updates logged-in users' entry address
when the logged-in user's address changes.

## Entry expiry thoughts

User logs in,
login signal puts entry in admin set.

Admin user has access to admin ports on the host.

User's entry expires
before the admin user logs out.

Cleanup runs and removes the user's entry
from the admin set.

Admin user no longer has access to admin ports on the host.

### Logout

Admin user logs out.

Session delete signal tries to remove
the entry from the admin set
but the entry no longer exists.

Firewall raises 404.

Admin user loses access to admin ports
when clear runs,
but if the common app expects 404
in the delete signal,
there's no problem.

### Address change

Admin user's address changes.

Middleware detects the change
when the user navigates to the admin trigger page
and tries to update the entry's address,
but the entry no longer exists.

Firewall re-adds the entry
and the user re-gains access to the admin ports.

Admin user loses access to admin ports
when clear runs,
but re-gains it
when they access the admin trigger page.

No problem.

### No address change

Same as address change.

### Session deletion

Same as logout.
