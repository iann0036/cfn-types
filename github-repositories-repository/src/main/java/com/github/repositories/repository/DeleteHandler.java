package com.github.repositories.repository;

import java.io.IOException;
import java.nio.charset.Charset;

import com.amazonaws.cloudformation.proxy.AmazonWebServicesClientProxy;
import com.amazonaws.cloudformation.proxy.Logger;
import com.amazonaws.cloudformation.proxy.OperationStatus;
import com.amazonaws.cloudformation.proxy.ProgressEvent;
import com.amazonaws.cloudformation.proxy.ResourceHandlerRequest;

import org.apache.commons.codec.binary.Base64;
import org.apache.http.HttpHeaders;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpDelete;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClientBuilder;

public class DeleteHandler extends BaseHandler<CallbackContext> {

    static CloseableHttpClient httpclient = HttpClientBuilder.create().build();
    static CloseableHttpResponse httpresponse;

    private static void deleteRepo(String owner, String name, String password) throws IOException {
        HttpDelete request = new HttpDelete("https://api.github.com/repos/" + owner + "/" + name);

        String auth = owner + ":" + password;
        byte[] encodedAuth = Base64.encodeBase64(auth.getBytes(Charset.forName("ISO-8859-1")));
        String authHeader = "Basic " + new String(encodedAuth);

        request.setHeader(HttpHeaders.AUTHORIZATION, authHeader);

        httpresponse = httpclient.execute(request);
        int statusCode = httpresponse.getStatusLine().getStatusCode();

        if (statusCode != 204) {
            throw new IOException("Unexpected status code returned: " + Integer.toString(statusCode));
        }
    }

    @Override
    public ProgressEvent<ResourceModel, CallbackContext> handleRequest(
        final AmazonWebServicesClientProxy proxy,
        final ResourceHandlerRequest<ResourceModel> request,
        final CallbackContext callbackContext,
        final Logger logger) {

        final ResourceModel model = request.getDesiredResourceState();

        try {
            String owner = model.getUsername();
            if (model.getOwner() != null) {
                owner = model.getOwner();
            }

            deleteRepo(owner, model.getName(), model.getPassword());

            return ProgressEvent.<ResourceModel, CallbackContext>builder()
                .resourceModel(model)
                .status(OperationStatus.SUCCESS)
                .build();
        } catch (IOException e) {
            logger.log(e.getMessage());
        }

        return ProgressEvent.<ResourceModel, CallbackContext>builder()
            .resourceModel(model)
            .status(OperationStatus.FAILED)
            .message("An internal error occurred")
            .build();
    }
}
