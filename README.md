This is a package for reading RGB bands from a recently uploaded Landsat scene and writing it out to a thumbnail. It uses
a notification from AWS SNS to initiate a Lambda function which does the image stacking, color correction and writeout.

#### Running the code
To build the code, use

``` sam build --use-container ```

It uses a python3.8 container. The required libraries listed in the `requirements.txt` file and are mostly related to `rasterio`.
To run the code deploy it to an AWS Lambda function instance with get and put permissions as listed in the `template.yaml` file. 
I could not get the rasterio installation to work as a layer yet.

The test event is stored under `message.json`. It mimics the upload of a new scene to the Landsat PDS bucket.
Triggering the test event will write the raster thumbnail to an S3 bucket, here named `testpushkarbucket`. You want to change
this to your bucket in the template file.


### Issues
1. No unit tests yet
2. The raterio open function is making a lot of calls to S3 looking for xml, msk, ovr and other supplementary files. Need to find
some way to minimize these calls, the `GEOREF_SOURCES='internal'` statement doesn't seem to work.
3. Need to setup a better deployment method, manually zipping and uploading is slow and painful.