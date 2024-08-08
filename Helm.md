# Helm Values Guide

Let's look at helm values used in values.yaml file & configure them as suitable

For yaml object respentation, JS based dot notation is used in the md. E.g.
```
image:
  repository: value
```
is getting represented as
```
image.repository
```

- ReplicaCount
  - It is used to specify the number of replicas needed for a particular pod. 
  - This value is used in the replica key present in the Deployment and Pod yaml file
- image.repository
  - Your container/docker image
- image.pullPolicy
  - Weather to fetch the image from registry or not and by which approach
  - Options available
    - IfNotPresent: Pull only if not already present locally
    - Always: Pull from container registery, every time the container is launched
    - Never: Use locally available image if present, otherwise fail
- image.tag
  - Tag of the image
- imagePullSecrets:
  - Secret file name containing the credentials to be used for authenticating & auhorization during pull image call to private registry
  - Secret must be in the same namespace
  - There is alternative way, where we can attach the secret to serviceAccount and we won't need to specify this field in this file since it will be automatically loaded by the serviceAccount usage. For more info [refer](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/#add-imagepullsecrets-to-a-service-account)
- nameOverride
  - You can override the name of this deployment which is by default the same as mentioned in the Chart.yaml name field
- fullnameOverride
  - Helm attaches a release tag to you provided name and calls it fullname, you can override that too.
- seviceAccount.create
  - Whether to create a service account automatically
- serviceAccount.automount
  - Whether to mount the api credentials of the service account automatically inside the pod
- serviceAccount.annotations
  - Annotations
- serviceAccount.name: 
  - if name is set, and it exists, it attaches that service account
  - If not set and create is true, a name is generated using the fullname template
- podAnnotations
  - annotations are metadata key/value pair, similar to labels, but annotations are not used for matching and identifying the resources.
  - annotations can be release build, timestamp - only for information purpose or it can be imageRegistry url which can be used by the k8s to call correct host for fetching the image
- podLabels
  - add labels to your pod, which are key/value pair
  - labels is metadata
  - They can be used to attach multiple resources to each other using `matchSelector` tags
- service.type
  - Services provides networking capabilities to the pod
  - Type of service to be created
    - ClusterIP: Exposed on cluster-internal IP, making it reachable only within the cluster. Default option
    - NodePort: Expose pod on Node's IP with the static port mentioned here.
    - LoadBalancer: Expose the service using external load balancer. Can be integrated with cloud provider options
    - ExternalName: Will add details
- service.port
  - Port used by the service
  - Helm chart default configugration makes the service.port and service.targetPort parameter same. It makes things consistent, you can alter your helm chart as per your need though
- ingress.enabled
  - Enable inress or not (true/false)
- ingress.className
  - Specify name of ingress control being used, it can be aws lb, nginx etc.
- ingress.annotations
  - annotations to configure your load balancer properties
- ingress.hosts.host (Array)
  - domain name to be used by your load balancer
- ingress.hosts.paths.path
  - Load balancing based on path parameter
- ngress.hosts.paths.pathType
  - Type of path based redirecting.
  - It can be
    - Exact
    - Prefix
    - ImplementationSpecifc
- ingress.tls.secretName
  - Secret name which contains the tls credentials like cert and private key
- ingress.tls.hosts
  - This is same as ingress.hosts field (Will confirm)
- resources.limits.cpu
  - Max cpu allocation for this container
  - 100m means 100milli CPU equivalent to 1 cpu
- resources.limits.memory
  - Max memory allocation for this container
  - 128Mi means 128MebiByte memory
- resources.requests.cpu
  - Mininum cpu allocation for this container
  - 100m means 100milli CPU equivalent to 1 cpu
- resources.requests.memory
  - Mininum memory allocation for this container
  - 128Mi means 128MebiByte memory
- livenessProbe.httpGet
  - It specified the path & port to be used for checking liveness of the pod
- readinessProbe.httpGet
  - it is used initial to measure if pod is ready to accept connection, measuring readiness of the pod
- autoscaling.enabled
  - Enable HPA Or Not (true/false)
- autoscaling.minReplicas
  - minimum number of replicas a pod should have
- autoscaling.minReplicas
  - maximum number of replicas a pod can have
- autoscaling.targetCPUUtilizationPercentage
  - Percentage of CPU usage after which autoscaling(new replicas) should happen
- autoscaling.targetMemoryUtilizationPercentage
  - Percentage of Memory usage after which autoscaling(new replicas) should happen
- volumes.name
  - Name of volume to be attached
- volume.persistentVolumeClaim.claimName
  - PVC name to be used to accessing the volume based on those criteria. PVC & Volume creation should be done before running helm install command (Will see if I can add it to the charts folder)
- volumeMounts.name
  - Name of volume mount
- volumeMounts.mountPath
  - Pod location at which the volume should be mounted
- nodeSelector
  - Specify the matching label corresponding to the Node's label on which you want to run this pod specifically
  - By specifying the label key=value like `custom-label=custom-value` on Node and in this field here, we can forced the kube-scheduler to schedule this pod on a particular node
- tolerations
  - Toleration goes hand in hand with taints.
  - We can attacha  taint on a node with a certain property. E.g. `kubectl taint nodes node1 key1=value1:NoSchedule-`
  - Now no pod will be able to schedule onto node1 unless it has a matching toleration. E.g.
    ```yaml
      tolerations:
      key: "key1"
      operator: "Equal"
      value: "value1"
      effect: "NoSchedule"
    ```
  - Tolerations allow scheduling but don't guarantee scheduling
- affinity
  - More expressive type of nodeSelector, with more constraints
  - Types
    - nodeAffinity: Match label between Pod and Node
    - podAffinity: Match label between Pod and existing Pods running on a Node
    - podAntiAffinity: Same as podAffinity but does the inverse, tries to put matching label pods on different Node
```yaml
# ReplicaCount is used to specify the number of replicas needed for a particular pod
replicaCount: 1

image:
  repository: service-name # Your container/docker image 
  pullPolicy: Never # Weather to fetch the image from container registry or use the locally availables
  # Overrides the image tag whose default is the chart appVersion.
  tag: "latest"

imagePullSecrets: []
nameOverride: service-name
fullnameOverride: ""

serviceAccount:
  # Specifies whether a service account should be created
  create: false
  # Automatically mount a ServiceAccount's API credentials?
  automount: true
  # Annotations to add to the service account
  annotations: {}
  # The name of the service account to use.
  # If not set and create is true, a name is generated using the fullname template
  name: "nameOfServiceAccount"

podAnnotations: {}
podLabels:
  app: backend

podSecurityContext: {}
  # fsGroup: 2000

securityContext: {}
  # capabilities:
  #   drop:
  #   - ALL
  # readOnlyRootFilesystem: true
  # runAsNonRoot: true
  # runAsUser: 1000

service:
  type: ClusterIP
  port: 5000

ingress:
  enabled: true
  className: "nginx"  # Or any other lb
  annotations:
    nginx.ingress.kubernetes.io/enable-cors: "true"
    nginx.ingress.kubernetes.io/rewrite-target: /$2
    nginx.ingress.kubernetes.io/use-regex: "true"
  hosts:
    - host: host
      paths:
        - path: /api(/|$)(.*)
          pathType: ImplementationSpecific
  tls: []
  #  - secretName: chart-example-tls
  #    hosts:
  #      - chart-example.local

resources:
  limits:
    cpu: 100m
    memory: 128Mi
  requests:
    cpu: 100m
    memory: 128Mi

livenessProbe:
  httpGet:
    path: /
    port: http
readinessProbe:
  httpGet:
    path: /
    port: http

autoscaling:
  enabled: true
  minReplicas: 1
  maxReplicas: 10
  targetCPUUtilizationPercentage: 5
  targetMemoryUtilizationPercentage: 50

# Additional volumes on the output Deployment definition.
volumes:
  - name: vol1
    persistentVolumeClaim:
      claimName: backend-volume-claim

# Additional volumeMounts on the output Deployment definition.
volumeMounts:
- name: vol1
  mountPath: "/data"

nodeSelector: {}

tolerations: []

affinity: {}

```