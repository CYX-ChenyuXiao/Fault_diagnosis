image="tdu2/$(basename $PWD):latest"
echo "building image "${image}
docker build -t ${image} .
echo "success"