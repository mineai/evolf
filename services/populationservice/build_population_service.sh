
cp -r framework services/populationservice/
cp -r servicecommon services/populationservice/
cp -r search_space services/populationservice/

cd services/populationservice/

docker build -t population_server .

rm -r framework
rm -r servicecommon
rm -r searchspace