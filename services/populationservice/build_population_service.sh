
cp -r framework services/populationservice/
cp -r servicecommon services/populationservice/
cp -r searchspace services/populationservice/
cp -r lossconstructor services/populationservice/

cd services/populationservice/

docker build -t population_server .

rm -r framework
rm -r servicecommon
rm -r searchspace
rm -r lossconstructor
