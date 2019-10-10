package com.ianmckay.s3.object;

import java.io.Serializable;
import java.io.ByteArrayInputStream;

import com.amazonaws.auth.AWSCredentials;
import com.amazonaws.auth.AWSCredentialsProvider;
import com.amazonaws.auth.AWSStaticCredentialsProvider;
import com.amazonaws.cloudformation.proxy.AmazonWebServicesClientProxy;
import com.amazonaws.cloudformation.proxy.Logger;
import com.amazonaws.cloudformation.proxy.ProgressEvent;
import com.amazonaws.cloudformation.proxy.OperationStatus;
import com.amazonaws.cloudformation.proxy.ResourceHandlerRequest;
import com.amazonaws.services.s3.AmazonS3ClientBuilder;
import com.amazonaws.services.s3.model.PutObjectRequest;
import com.amazonaws.services.s3.model.PutObjectResult;
import com.amazonaws.services.s3.model.CannedAccessControlList;
import com.amazonaws.services.s3.model.ObjectMetadata;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.securitytoken.AWSSecurityTokenService;
import com.amazonaws.services.securitytoken.AWSSecurityTokenServiceClientBuilder;
import com.amazonaws.services.securitytoken.model.GetCallerIdentityRequest;

public class CreateHandler extends BaseHandler<CallbackContext> {

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
            ByteArrayInputStream bs = new ByteArrayInputStream(model.getBody().getBytes());
            ObjectMetadata metadata = new ObjectMetadata();
            
            AWSCredentials creds = getCredentials(proxy);
            
            AmazonS3 client = AmazonS3ClientBuilder.standard()
                    .withCredentials(new AWSStaticCredentialsProvider(creds))
                    .build();

            PutObjectRequest putObjectRequest = new PutObjectRequest(bucketName, keyName, bs, metadata);

            String aclString = model.getTarget().getACL();
            switch(aclString) {
                case "private":
                    putObjectRequest.setCannedAcl(CannedAccessControlList.Private);
                    break;
                case "public-read":
                    putObjectRequest.setCannedAcl(CannedAccessControlList.PublicRead);
                    break;
                case "public-read-write":
                    putObjectRequest.setCannedAcl(CannedAccessControlList.PublicReadWrite);
                    break;
                case "aws-exec-read":
                    putObjectRequest.setCannedAcl(CannedAccessControlList.AwsExecRead);
                    break;
                case "authenticated-read":
                    putObjectRequest.setCannedAcl(CannedAccessControlList.AuthenticatedRead);
                    break;
                case "bucket-owner-read":
                    putObjectRequest.setCannedAcl(CannedAccessControlList.BucketOwnerRead);
                    break;
                case "bucket-owner-full-control":
                    putObjectRequest.setCannedAcl(CannedAccessControlList.BucketOwnerFullControl);
                    break;
            }

            PutObjectResult putObjectResult = client.putObject(putObjectRequest);

            model.setETag(putObjectResult.getETag());
            if (keyName.charAt(0) != '/') {
                keyName = "/" + keyName;
            }
            model.setS3Url("s3://" + bucketName + keyName);

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
