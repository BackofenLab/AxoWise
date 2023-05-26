# OpenStack

To set up OpenStack, please follow the steps outlined below.
This documentation assumes that you have access to an OpenStack dashboard or want to register using deNBI.

### Registering for deNBI

1. If you wish to use deNBI, please request an invite link.
2. Once you receive the invite link, follow the instructions provided.
3. You will be redirected to the [deNBI](https://cloud.denbi.de/portal/webapp/#/) site.
4. On the deNBI site, you can also find a link to
   the [OpenStack](https://cloud.computational.bio.uni-giessen.de/dashboard/project/) dashboard. Which is the starting
   point for the setup-chapter.

### Setting Up Openstack

1. There is a helpful [tutorial](https://openmetal.io/docs/manuals/operators-manual/day-1/horizon/create-first-instance)
   available that provides a step-by-step explanation of how to create all the necessary components to get your server
   up and running.
   The tutorial concludes with SSH access to the server.

   > When creating the security groups, ensure that you initially set the remote IP Address to `0.0.0.0` to ensure that
   everything works. The security group settings can be easily adjusted later on.

2. Once done with installation you can use `ssh ubuntu@floating-ip` (e.g. `ssh ubuntu@134.176.27.91`) to connect to the
   server.