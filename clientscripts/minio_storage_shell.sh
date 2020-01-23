# Check the Environment Variables MINIO_ACCESS_KEY and MINIO_SECRET_KEY

if [ $MINIO_ENPOINT == "" ]
then
    # Pack all files from ./data into a .tar file (tarfile documentation)
    # python3 -m tarfile -c data.tar data/

    # create a new bucket
    # s3cmd mb s3://tarfiles
    
    # Upload the .tar file to a bucket on MinIO ()
    # s3cmd put data.tar s3://tarfiles
else
    # echo Please add credentials



