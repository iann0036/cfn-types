package com.mycorp.ec2.keypair;

import com.amazonaws.cloudformation.proxy.AmazonWebServicesClientProxy;
import com.amazonaws.cloudformation.proxy.Logger;
import com.amazonaws.cloudformation.proxy.OperationStatus;
import com.amazonaws.cloudformation.proxy.ProgressEvent;
import com.amazonaws.cloudformation.proxy.ResourceHandlerRequest;
import com.amazonaws.services.ec2.model.ImportKeyPairRequest;
import com.amazonaws.services.ec2.model.ImportKeyPairResult;
import com.amazonaws.services.ec2.model.DeleteKeyPairRequest;
import com.amazonaws.services.ec2.model.DeleteKeyPairResult;
import com.amazonaws.services.ec2.model.KeyPairInfo;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;
import static org.mockito.Mockito.any;

@ExtendWith(MockitoExtension.class)
public class UpdateHandlerTest {

    @Mock
    private AmazonWebServicesClientProxy proxy;

    @Mock
    private Logger logger;

    @BeforeEach
    public void setup() {
        proxy = mock(AmazonWebServicesClientProxy.class);
        logger = mock(Logger.class);
    }

    @Test
    public void handleRequest_SimpleSuccess() {
        when(proxy.injectCredentialsAndInvoke(any(DeleteKeyPairRequest.class), any())).thenReturn(
            new DeleteKeyPairResult()
        );
        when(proxy.injectCredentialsAndInvoke(any(ImportKeyPairRequest.class), any())).thenReturn(
            new ImportKeyPairResult()
                .withKeyName("mykey")
                .withKeyFingerprint("88:e3:48:8d:3d:61:a3:5c:0b:a3:f8:41:ee:d2:5d:22")
        );

        final UpdateHandler handler = new UpdateHandler();

        final ResourceModel previousModel = ResourceModel.builder()
            .keyName("mykey2")
            .publicKey("ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDU9sjjIO7wdRJT495agnFi++KlKjHKEBpCnHYHJB4U9+1tZPvSkrRI0nD8LULYIgFVi+VbBxlzLol376kAYK1iCE68B5p1DGRV1ecoJgmJSiBGjEz5BDS1ineLToJtLh2Ccb2xQF1Pe8dcyP8Ogu+/AAG5QMyPK+taXcU20ZlprQ7z8UlRsOdTHiYWFJH8NXkGCihLTBaYNDEz6wmgHTsN5HWkaNz32mH/AEJJfiN7rAmKmbk5DKtJccjP9Wp4mnvXWg22EFowIafksLbxc+P+xQgZN+9Coz+HSo/ePFHiLB7YZoEusMBgAY/UttJbNPoEhSitNuDkcHAUAz9ElWMl")
            .build();

        final ResourceModel model = ResourceModel.builder()
            .keyName("mykey")
            .publicKey("ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDU9sjjIO7wdRJT495agnFi++KlKjHKEBpCnHYHJB4U9+1tZPvSkrRI0nD8LULYIgFVi+VbBxlzLol376kAYK1iCE68B5p1DGRV1ecoJgmJSiBGjEz5BDS1ineLToJtLh2Ccb2xQF1Pe8dcyP8Ogu+/AAG5QMyPK+taXcU20ZlprQ7z8UlRsOdTHiYWFJH8NXkGCihLTBaYNDEz6wmgHTsN5HWkaNz32mH/AEJJfiN7rAmKmbk5DKtJccjP9Wp4mnvXWg22EFowIafksLbxc+P+xQgZN+9Coz+HSo/ePFHiLB7YZoEusMBgAY/UttJbNPoEhSitNuDkcHAUAz9ElWMl")
            .build();

        final ResourceHandlerRequest<ResourceModel> request = ResourceHandlerRequest.<ResourceModel>builder()
            .previousResourceState(previousModel)
            .desiredResourceState(model)
            .build();

        final ProgressEvent<ResourceModel, CallbackContext> response
            = handler.handleRequest(proxy, request, null, logger);

        assertThat(response).isNotNull();
        assertThat(response.getStatus()).isEqualTo(OperationStatus.SUCCESS);
        assertThat(response.getCallbackContext()).isNull();
        assertThat(response.getCallbackDelaySeconds()).isEqualTo(0);
        assertThat(response.getResourceModel()).isEqualTo(request.getDesiredResourceState());
        assertThat(response.getResourceModels()).isNull();
        assertThat(response.getMessage()).isNull();
        assertThat(response.getErrorCode()).isNull();
    }
}
