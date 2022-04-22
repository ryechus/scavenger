# Scavenger Image Service

The Scavenger Image Service accepts image uploads and serves images that have been uploaded.
The service is meant to be an abstraction of image storage for a Django/Wagtail application.

## High Level Needs

* Performant -- low latency
* Fault tolerant
* Small interface
* Expressive
  * Should be able to resize images by changing url query string params and stuff -- think cloudinary

**Performant**

Let's start with Python to get an MVP while ironing out the API design. Eventually we will want this to
be in something that is faster. Go maybe? Rust?


**Fault Tolerant**

Gunicorn could be helpful here. We already have a k8s cluster so getting more capacity isn't a big deal.
There should be some caching...eventually a CDN?

**Small Interface**

There should really only be one endpoint.

    POST https://images.dtlascavenger.com/ <- uploads an image -- images do not overwrite
    GET https://images.dtlascavenger.com/<image_filename>.<image_extension>

**Expressive**

Users should be able to use the service as a resizing service; similar to cloudinary.

* resizing width and height independently
* resizing width and height while maintaining proportions
* top, left, bottom, right offset (cropping)
* quality
