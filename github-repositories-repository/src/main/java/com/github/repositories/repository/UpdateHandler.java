package com.github.repositories.repository;

import java.io.IOException;

import com.amazonaws.cloudformation.proxy.AmazonWebServicesClientProxy;
import com.amazonaws.cloudformation.proxy.Logger;
import com.amazonaws.cloudformation.proxy.OperationStatus;
import com.amazonaws.cloudformation.proxy.ProgressEvent;
import com.amazonaws.cloudformation.proxy.ResourceHandlerRequest;

import org.eclipse.egit.github.core.Repository;
import org.eclipse.egit.github.core.User;
import org.eclipse.egit.github.core.service.RepositoryService;

public class UpdateHandler extends BaseHandler<CallbackContext> {

    @Override
    public ProgressEvent<ResourceModel, CallbackContext> handleRequest(
        final AmazonWebServicesClientProxy proxy,
        final ResourceHandlerRequest<ResourceModel> request,
        final CallbackContext callbackContext,
        final Logger logger) {

        final ResourceModel model = request.getDesiredResourceState();
        final ResourceModel previousModel = request.getPreviousResourceState();

        RepositoryService service = new RepositoryService();
        service.getClient().setCredentials(model.getUsername(), model.getPassword());

        if (model.getOwner() != null && !model.getOwner().equals(previousModel.getOwner())) {
            return ProgressEvent.<ResourceModel, CallbackContext>builder()
                .resourceModel(previousModel)
                .status(OperationStatus.FAILED)
                .message("Update owner currently not supported")
                .build();
        }
        if (model.getName() != null && !model.getName().equals(previousModel.getName())) {
            return ProgressEvent.<ResourceModel, CallbackContext>builder()
                .resourceModel(previousModel)
                .status(OperationStatus.FAILED)
                .message("Update name currently not supported")
                .build();
        }

        try {
            String previousOwner = previousModel.getUsername();
            if (previousModel.getOwner() != null) {
                previousOwner = previousModel.getOwner();
            }

            Repository repository = service.getRepository(previousOwner, previousModel.getName());
            Repository response;

            if (model.getOwner() != null) {
                User owner = new User().setLogin(model.getOwner());
                repository.setOwner(owner);
            }
            if (model.getDescription() != null) {
                repository.setDescription(model.getDescription());
            }
            if (model.getIsPrivate() != null) {
                repository.setPrivate(model.getIsPrivate());
            }
            if (model.getHomepage() != null) {
                repository.setHomepage(model.getHomepage());
            }
            if (model.getHasIssues() != null) {
                repository.setHasIssues(model.getHasIssues());
            }
            if (model.getHasWiki() != null) {
                repository.setHasWiki(model.getHasWiki());
            }
            repository.setName(model.getName());

            response = service.editRepository(repository);

            if (model.getOwner() == null) {
                model.setOwner(response.getOwner().getLogin());
            }

            model.setRepoPath(model.getOwner() + "/" + model.getName());

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
