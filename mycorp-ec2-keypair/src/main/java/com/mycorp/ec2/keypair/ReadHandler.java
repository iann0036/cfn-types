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

import java.util.List;

public class ReadHandler extends BaseHandler<CallbackContext> {

    @Override
    public ProgressEvent<ResourceModel, CallbackContext> handleRequest(
        final AmazonWebServicesClientProxy proxy,
        final ResourceHandlerRequest<ResourceModel> request,
        final CallbackContext callbackContext,
        final Logger logger) {

        final ResourceModel model = request.getDesiredResourceState();

        String errorMessage = "An internal error occurred";

        try {
            AmazonEC2 client = AmazonEC2ClientBuilder.standard().build();
            
            DescribeKeyPairsRequest describeKeyPairsRequest = new DescribeKeyPairsRequest().withKeyNames(model.getKeyName());

            DescribeKeyPairsResult describeKeyPairsResult = proxy.injectCredentialsAndInvoke(describeKeyPairsRequest, client::describeKeyPairs);

            List<KeyPairInfo> keyPairs = describeKeyPairsResult.getKeyPairs();
            
            if (keyPairs.size() < 1) {
                errorMessage = "Key pair could not be found";
            } else if (keyPairs.size() == 1) {
                model.setFingerprint(keyPairs.get(0).getKeyFingerprint());

                return ProgressEvent.<ResourceModel, CallbackContext>builder()
                    .resourceModel(model)
                    .status(OperationStatus.SUCCESS)
                    .build();
            } else {
                errorMessage = "More than one key pair was found"; // shouldn't be possible
            }
        } catch (Exception e) {
            logger.log(e.getMessage());
        }

        return ProgressEvent.<ResourceModel, CallbackContext>builder()
            .resourceModel(model)
            .status(OperationStatus.FAILED)
            .message(errorMessage)
            .build();
    }
}
