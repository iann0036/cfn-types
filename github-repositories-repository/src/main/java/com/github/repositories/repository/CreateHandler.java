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

public class CreateHandler extends BaseHandler<CallbackContext> {

    @Override
    public ProgressEvent<ResourceModel, CallbackContext> handleRequest(
        final AmazonWebServicesClientProxy proxy,
        final ResourceHandlerRequest<ResourceModel> request,
        final CallbackContext callbackContext,
        final Logger logger) {

        final ResourceModel model = request.getDesiredResourceState();

        RepositoryService service = new RepositoryService();
        service.getClient().setCredentials(model.getUsername(), model.getPassword());
        Repository repository = new Repository();

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

        try {
            Repository response;

            if (model.getOwner() != null) {
                response = service.createRepository(model.getOwner(), repository);
            } else {
                response = service.createRepository(repository);
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
