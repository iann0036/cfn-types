package com.ianmckay.s3.object;

import java.io.ByteArrayInputStream;
import java.io.Serializable;

import com.amazonaws.AmazonWebServiceResult;
import com.amazonaws.ResponseMetadata;
import com.amazonaws.auth.AWSCredentials;
import com.amazonaws.auth.AWSCredentialsProvider;
import com.amazonaws.auth.AWSStaticCredentialsProvider;
import com.amazonaws.auth.BasicSessionCredentials;
import com.amazonaws.cloudformation.proxy.AmazonWebServicesClientProxy;
import com.amazonaws.cloudformation.proxy.Logger;
import com.amazonaws.cloudformation.proxy.ProgressEvent;
import com.amazonaws.cloudformation.proxy.OperationStatus;
import com.amazonaws.cloudformation.proxy.ResourceHandlerRequest;
import com.amazonaws.services.s3.AmazonS3ClientBuilder;
import com.amazonaws.services.s3.model.CannedAccessControlList;
import com.amazonaws.services.s3.model.DeleteObjectRequest;
import com.amazonaws.services.s3.model.DeleteObjectsResult;
import com.amazonaws.services.s3.model.ObjectMetadata;
import com.amazonaws.services.s3.model.PutObjectRequest;
import com.amazonaws.services.s3.model.PutObjectResult;
import com.amazonaws.services.securitytoken.AWSSecurityTokenService;
import com.amazonaws.services.securitytoken.AWSSecurityTokenServiceClientBuilder;
import com.amazonaws.services.securitytoken.model.Credentials;
import com.amazonaws.services.securitytoken.model.GetCallerIdentityRequest;
import com.amazonaws.services.securitytoken.model.GetSessionTokenRequest;
import com.amazonaws.services.securitytoken.model.GetSessionTokenResult;

import software.amazon.awssdk.awscore.AwsResponse;

import com.amazonaws.services.s3.AmazonS3;

public class DeleteHandler extends BaseHandler<CallbackContext> {

    // Create a fake AWS request and save the proxy credentials for use later
    private class FakeRequest extends GetCallerIdentityRequest implements Serializable, Cloneable {
        static final long serialVersionUID = 0;

        public AWSCredentials creds;

        @Override
        public void setRequestCredentialsProvider(AWSCredentialsProvider credentialsProvider) {
            creds = credentialsProvider.getCredentials();
        }
    }

    private AWSCredentials getCredentials(AmazonWebServicesClientProxy proxy) {
        FakeRequest req = new FakeRequest();

        try {
            AWSSecurityTokenService stsclient = AWSSecurityTokenServiceClientBuilder.standard().build();
            proxy.injectCredentialsAndInvoke(req, stsclient::getCallerIdentity);
        } catch(Exception e) { ; }

        return req.creds;
    }

    @Override
    public ProgressEvent<ResourceModel, CallbackContext> handleRequest(
        final AmazonWebServicesClientProxy proxy,
        final ResourceHandlerRequest<ResourceModel> request,
        final CallbackContext callbackContext,
        final Logger logger) {

        final ResourceModel model = request.getDesiredResourceState();

        try {
            String bucketName = model.getTarget().getBucket();
            String keyName = model.getTarget().getKey();
            
            AWSCredentials creds = getCredentials(proxy);
            
            AmazonS3 client = AmazonS3ClientBuilder.standard()
                    .withCredentials(new AWSStaticCredentialsProvider(creds))
                    .build();

            DeleteObjectRequest deleteObjectRequest = new DeleteObjectRequest(bucketName, keyName);

            client.deleteObject(deleteObjectRequest);

            return ProgressEvent.<ResourceModel, CallbackContext>builder()
                .resourceModel(model)
                .status(OperationStatus.SUCCESS)
                .build();
        } catch (Exception e) {
            logger.log(e.getMessage());
        }

        return ProgressEvent.<ResourceModel, CallbackContext>builder()
            .resourceModel(model)
            .status(OperationStatus.FAILED)
            .message("An internal error occurred")
            .build();
    }
}
