package com.mycorp.ec2.keypair;

import com.amazonaws.cloudformation.proxy.AmazonWebServicesClientProxy;
import com.amazonaws.cloudformation.proxy.Logger;
import com.amazonaws.cloudformation.proxy.ProgressEvent;
import com.amazonaws.cloudformation.proxy.OperationStatus;
import com.amazonaws.cloudformation.proxy.ResourceHandlerRequest;
import com.amazonaws.services.ec2.model.DescribeKeyPairsRequest;
import com.amazonaws.services.ec2.model.DescribeKeyPairsResult;
import com.amazonaws.services.ec2.AmazonEC2;
import com.amazonaws.services.ec2.AmazonEC2ClientBuilder;
import com.amazonaws.services.ec2.model.KeyPair;
import com.amazonaws.services.ec2.model.KeyPairInfo;

import java.util.ArrayList;
import java.util.List;

public class ListHandler extends BaseHandler<CallbackContext> {

    @Override
    public ProgressEvent<ResourceModel, CallbackContext> handleRequest(
        final AmazonWebServicesClientProxy proxy,
        final ResourceHandlerRequest<ResourceModel> request,
        final CallbackContext callbackContext,
        final Logger logger) {

        final List<ResourceModel> models = new ArrayList<>();
        
        try {
            AmazonEC2 client = AmazonEC2ClientBuilder.standard().build();
            
            DescribeKeyPairsRequest describeKeyPairsRequest = new DescribeKeyPairsRequest();

            DescribeKeyPairsResult describeKeyPairsResult = proxy.injectCredentialsAndInvoke(describeKeyPairsRequest, client::describeKeyPairs);
            
            for (KeyPairInfo keyPair : describeKeyPairsResult.getKeyPairs()) {
                ResourceModel resourceModel = new ResourceModel();

                resourceModel.setKeyName(keyPair.getKeyName());
                resourceModel.setFingerprint(keyPair.getKeyFingerprint());

                models.add(resourceModel);
            }

            return ProgressEvent.<ResourceModel, CallbackContext>builder()
                .resourceModels(models)
                .status(OperationStatus.SUCCESS)
                .build();
        } catch (Exception e) {
            logger.log(e.getMessage());
        }

        return ProgressEvent.<ResourceModel, CallbackContext>builder()
            .resourceModels(models)
            .status(OperationStatus.FAILED)
            .message("An internal error occurred")
            .build();
    }
}
