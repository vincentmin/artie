docker build --target=runtime . -t artie:latest
docker tag artie:latest us-central1-docker.pkg.dev/artie-450714/artie/artie-image:latest

# Optionally push to ghcr.io
#docker tag artie:latest ghcr.io/vincentmin/artie/artie:latest
#docker push ghcr.io/vincentmin/artie/artie:latest

gcloud init
gcloud iam service-accounts create artie-rijks-museum
gcloud projects add-iam-policy-binding artie-450714 \
    --member="serviceAccount:artie-rijks-museum@artie-450714.iam.gserviceaccount.com" \
    --role="roles/run.developer"
gcloud projects add-iam-policy-binding artie-450714 \
    --member="serviceAccount:artie-rijks-museum@artie-450714.iam.gserviceaccount.com" \
    --role="roles/iam.serviceAccountUser"
gcloud projects add-iam-policy-binding artie-450714 \
    --member="serviceAccount:artie-rijks-museum@artie-450714.iam.gserviceaccount.com" \
    --role="roles/artifactregistry.reader"

gcloud artifacts repositories create artie \
    --repository-format=docker \
    --location=us-central1 \
    --description="Artie Rijks Museum" \
    --async

gcloud auth configure-docker us-central1-docker.pkg.dev
docker push us-central1-docker.pkg.dev/artie-450714/artie/artie-image:latest