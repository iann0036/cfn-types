package com.pagerduty.resources.service;

import com.amazonaws.cloudformation.proxy.AmazonWebServicesClientProxy;
import com.amazonaws.cloudformation.proxy.Logger;
import com.amazonaws.cloudformation.proxy.ProgressEvent;
import com.amazonaws.cloudformation.proxy.OperationStatus;
import com.amazonaws.cloudformation.proxy.ResourceHandlerRequest;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.net.URL;

import java.util.List;
import java.util.Map;
import java.util.HashMap;

import javax.net.ssl.HttpsURLConnection;

import javax.xml.bind.annotation.*;
import javax.xml.bind.JAXBContext;
import javax.xml.bind.Marshaller;

import org.eclipse.persistence.jaxb.JAXBContextFactory;
import org.eclipse.persistence.jaxb.JAXBContextProperties;
import java.io.StringWriter;

public class CreateHandler extends BaseHandler<CallbackContext> {

    @XmlRootElement(name="service")
    @XmlAccessorType(XmlAccessType.FIELD)
    private static class PagerDutyCreateRequest {

        public String toJSON() throws Exception {
            Map<String, Object> properties = new HashMap<>();
            properties.put(JAXBContextProperties.MEDIA_TYPE, "application/json");
            properties.put(JAXBContextProperties.JSON_INCLUDE_ROOT, true);

            //Create a Context using the properties
            JAXBContext jaxbContext = JAXBContextFactory.createContext(new Class[] {PagerDutyCreateRequest.class}, properties);
            Marshaller marshaller = jaxbContext.createMarshaller();
            StringWriter sw = new StringWriter();
            marshaller.marshal(this, sw);

            return sw.toString();
        }

        @XmlAccessorType(XmlAccessType.FIELD)
        public static class EscalationPolicy {

            @XmlAttribute
            public String id;

            @XmlAttribute
            public String type;

        }

        @XmlAccessorType(XmlAccessType.FIELD)
        public static class IncidentUrgencyRule {

            @XmlAccessorType(XmlAccessType.FIELD)
            public static class UrgencyType {

                @XmlAttribute
                public String type;

                @XmlAttribute
                public String urgency;

            }

            @XmlElement
            public UrgencyType during_support_hours;

            @XmlElement
            public UrgencyType outside_support_hours;

            @XmlAttribute
            public String type;

        }

        @XmlAccessorType(XmlAccessType.FIELD)
        public static class SupportHours {

            @XmlAttribute
            public String type;
            
            @XmlAttribute
            public String time_zone;
            
            @XmlAttribute
            public String start_time;
            
            @XmlAttribute
            public String end_time;
            
            @XmlAttribute
            public List<Integer> days_of_week;

        }

        @XmlAccessorType(XmlAccessType.FIELD)
        public static class ScheduledActions {

            @XmlAccessorType(XmlAccessType.FIELD)
            public static class At {

                @XmlAttribute
                public String type;

                @XmlAttribute
                public String name;
                
            }

            @XmlAttribute
            public String type;

            @XmlAttribute
            public String to_urgency;

            @XmlElement
            public At at;
            
        }

        @XmlElement
        public EscalationPolicy escalation_policy;

        @XmlElement
        public IncidentUrgencyRule incident_urgency_rule;

        @XmlElement
        public SupportHours support_hours;

        @XmlElement
        public ScheduledActions scheduled_actions;

        @XmlAttribute
        public String type;

        @XmlAttribute
        public String name;

        @XmlAttribute
        public String description;

        @XmlAttribute
        public Integer auto_resolve_timeout;

        @XmlAttribute
        public Integer acknowledgement_timeout;

        @XmlAttribute
        public String status;

        @XmlAttribute
        public String alert_creation;

        @XmlAttribute
        public String alert_grouping;

        @XmlAttribute
        public Integer alert_grouping_timeout;

    }

    private void createService(PagerDutyCreateRequest pagerDutyCreateRequest, String token) throws Exception {
		String url = "https://api.pagerduty.com/services";
		URL obj = new URL(url);
		HttpsURLConnection con = (HttpsURLConnection) obj.openConnection();

		con.setRequestMethod("POST");
        con.setRequestProperty("Content-Type", "application/json");
        con.setRequestProperty("Authorization", "Token token=" + token);
        con.setRequestProperty("Accept", "application/vnd.pagerduty+json;version=2");
        
        String jsonString = pagerDutyCreateRequest.toJSON();
		
		con.setDoOutput(true);
		DataOutputStream wr = new DataOutputStream(con.getOutputStream());
		wr.writeBytes(jsonString);
		wr.flush();
		wr.close();

		int responseCode = con.getResponseCode();

		BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
		String inputLine;
		StringBuffer response = new StringBuffer();

		while ((inputLine = in.readLine()) != null) {
			response.append(inputLine);
		}
		in.close();
		
		System.out.println(response.toString());
	}

    @Override
    public ProgressEvent<ResourceModel, CallbackContext> handleRequest(
        final AmazonWebServicesClientProxy proxy,
        final ResourceHandlerRequest<ResourceModel> request,
        final CallbackContext callbackContext,
        final Logger logger) {

        final ResourceModel model = request.getDesiredResourceState();

        try {
            PagerDutyCreateRequest pagerDutyCreateRequest = new PagerDutyCreateRequest();

            pagerDutyCreateRequest.name = model.getName();
            pagerDutyCreateRequest.type = "service";
            pagerDutyCreateRequest.escalation_policy = new PagerDutyCreateRequest.EscalationPolicy();
            pagerDutyCreateRequest.escalation_policy.type = "escalation_policy_reference";
            pagerDutyCreateRequest.escalation_policy.id = model.getEscalationPolicy();

            createService(pagerDutyCreateRequest, model.getAuthorizationToken());

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
                .build();
    }
}
