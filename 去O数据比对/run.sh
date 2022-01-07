for a in {61..90}
do
    start=$[(a-1)*50000+1]
    end=$[(a*50000)]
    echo $start $end
    nohup python CompareData.py  $start $end &
    sleep  1
done
