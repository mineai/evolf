cp framework services/population_service
cp servicecommon services/population_service
cp search_space services/population_service
cp setup services/population_service

cd services/population_service
docker build -t populaiton_server .

rm -r framework
rm -r servicecommon
rm -r search_space
rm -r setup