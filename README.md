# go-http-server-custom-write-buffer-patch
A patch that adds a configurable `WriteBufferSize` option to the Golang HTTP server

## Why this patch?
In some situations, you may need to adjust the default hard-coded write buffer size (currently 4 KB) of the Golang HTTP server.

Adjusting the default buffer size allows you to benefit from higher throughput and improving the performance of your HTTP servers.

## Why is the write buffer size hard coded?
At the present, the Golang HTTP server does not have an option that allows you to configure the write buffer size for unknown reasons.

Refer to the below related issues for more information on this matter:
- https://github.com/golang/go/issues/13870
- https://groups.google.com/g/golang-dev/c/OuFtcKEyGrg

## How to run the patch?
Simply, run `python patch_http_server.py` to execute the Python script of the patch.

## What does this patch do?
The patch will modify the `src/net/http/server.go` file of your Go installation to add a configurable `WriteBufferSize` option into the `http.Server` struct.

Then the patch will make the HTTP server connection manager use the configured `WriteBufferSize` instead of the default `4<<10` value.