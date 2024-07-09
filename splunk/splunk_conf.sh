## if you move the indexes bypass exit code 1
    OPTIMISTIC_ABOUT_FILE_LOCKING = 1
    ## located in splunk/etc/splunk-launch.conf
    ## this does mean the db have correct perms

## splunkforwarder linux config cli
    ./splunk set deploy-poll <deployment server>:8089
    ./splunk add forward-server <indexer>:9997