package com.mycorp.ec2.keypair;

import com.amazonaws.cloudformation.proxy.AmazonWebServicesClientProxy;
import com.amazonaws.cloudformation.proxy.Logger;
import com.amazonaws.cloudformation.proxy.ProgressEvent;
import com.amazonaws.cloudformation.proxy.OperationStatus;
import com.amazonaws.cloudformation.proxy.ResourceHandlerRequest;
import com.amazonaws.services.ec2.model.ImportKeyPairRequest;
import com.amazonaws.services.ec2.model.DeleteKeyPairRequest;
import com.amazonaws.services.ec2.model.ImportKeyPairResult;
import com.amazonaws.services.ec2.AmazonEC2;
import com.amazonaws.services.ec2.AmazonEC2ClientBuilder;

public class UpdateHandler extends BaseHandler<CallbackContext> {

    @Override
    public ProgressEvent<ResourceModel, CallbackContext> handleRequest(
        final AmazonWebServicesClientProxy proxy,
        final ResourceHandlerRequest<ResourceModel> request,
        final CallbackContext callbackContext,
        final Logger logger) {

        final ResourceModel model = request.getDesiredResourceState();
        final ResourceModel previousModel = request.getPreviousResourceState();
        
        try {
            AmazonEC2 client = AmazonEC2ClientBuilder.standard().build();
            
            ImportKeyPairRequest awsrequest = new ImportKeyPairRequest()
                .withKeyName(model.getKeyName())
                .withPublicKeyMaterial(model.getPublicKey());

            ImportKeyPairResult result = proxy.injectCredentialsAndInvoke(awsrequest, client::importKeyPair);
            
            DeleteKeyPairRequest deleteKeyPairRequest = new DeleteKeyPairRequest()
                .withKeyName(previousModel.getKeyName());

            proxy.injectCredentialsAndInvoke(deleteKeyPairRequest, client::deleteKeyPair);

            model.setFingerprint(result.getKeyFingerprint());

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
