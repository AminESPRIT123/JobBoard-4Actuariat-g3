package tn.esprit.gateway;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
import org.springframework.cloud.gateway.route.RouteLocator;
import org.springframework.cloud.gateway.route.builder.RouteLocatorBuilder;
import org.springframework.cloud.loadbalancer.annotation.LoadBalancerClient;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
@EnableDiscoveryClient
@LoadBalancerClient(name = "candidat", configuration = CandidatRandomConfiguration.class)
public class GatewayApplication {

    public static void main(String[] args) {
        SpringApplication.run(GatewayApplication.class, args);
    }

    @Bean
    public RouteLocator gatewayRoutes(RouteLocatorBuilder builder) {
        return builder.routes()
                .route("candidat", route -> route
                        .path("/mic1/candidates", "/mic1/candidates/**")
                        .uri("lb://candidat"))
                .route("job", route -> route
                        .path("/mic2/jobs", "/mic2/jobs/**")
                        .filters(filters -> filters.rewritePath("^/mic2/", "/api/"))
                        .uri("http://localhost:8082"))
                .route("candidature", route -> route
                        .path("/mic3/candidature", "/mic3/candidature/**")
                        .uri("http://localhost:8085"))
                .route("meeting", route -> route
                        .path("/api/meetings", "/api/meetings/**")
                        .uri("lb://meeting"))
                .route("notification-info", route -> route
                        .path("/notification/info")
                        .filters(filters -> filters.rewritePath("^/notification/", "/"))
                        .uri("lb://notification"))
                .build();
    }
}