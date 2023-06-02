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

### Add another SSH User

Please follow [this tutorial](https://linuxhandbook.com/add-ssh-public-key-to-server/) and use the manual approach.

### Simple Deployment directly in Ubuntu using CronJobs

This deployment will pull the repository, rebuild and restart the server every night. It is a very simple setup, that
might not fit your needs! Please think about your deployment strategy first, before applying this blindly.

1. [Create a token for GitHub](https://stackoverflow.com/questions/2505096/clone-a-private-repository-github) to have
   clone and pull access to the private repository.
2. create a workspace with `mkdir workspace` and clone the repository into the workspace.
3. install the environment needed to run the server. This could be java/miniconda/neo4j/... and can be done using the
   Requirements.mk file
4. create a script that does the following steps (an example can be found in the Makefile)
    1. stop the server
    2. pull git changes
    3. install all dependencies
    4. build the project
    5. restart the server
5. run the script via a cronjob
    - create a cronjob by modifying the file of `crontab -e` (first read the boxes!)
    - to specify the time use [this website](https://crontab.guru/)
    - all other necessary commands are in the articles below
   > [be careful with the conda environment](https://unix.stackexchange.com/questions/454957/cron-job-to-run-under-conda-virtual-environment)

   > [be careful with the directory](https://stackoverflow.com/questions/8899737/crontab-run-in-directory)

### Restart the Server manually

If you can't wait for the cronjob to run, you might want to follow these steps to restart the server:

1. ssh into the server
2. `conda activate pgdb`
3. `cd workspace/protein-graph-database`
4. `git pull`
5. `make deployment`
