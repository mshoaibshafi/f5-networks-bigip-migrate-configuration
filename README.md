### f5-networks-bigip-migrate-configuration

Migrate BigIP configuration from one unit to another

There are severals (may be) easier ways to migrate bigip configuration from one unit to another, but i chose to use the following to accomplish this :

1. f5 sdk 
2. python 3.6

### Sequence 
1. Migrate Monitors
2. Migrate Pools
3. Migrate Profiles
4. Migrate Virtuals


### Environment
1. f5-sdk : 3.0.14
2. python : 3.6.5
3. BigIP version (both source and destination ) : 12.1.2 HF1

### disclaimer 

use at your own risk