import os
import pika
import traceback

def publish ():
    source_path = '/mnt/d/GenStore/sample-data-set/survey-results'
    rbt_srv = 'rabbit-queue'
    trgt_queue = 'new_files'

    try:
        # Get list of file paths to publish 
        fAr = os.listdir( source_path )

        print('Connecting to rabbit ',rbt_srv)
        with pika.BlockingConnection(pika.ConnectionParameters(rbt_srv)) as connection:
            channel = connection.channel()
            print('Connected')
            # Create queue if it doesn't 
            channel.queue_declare(queue=trgt_queue, durable=True)
            # Clear queue
            channel.queue_purge(queue=trgt_queue) 

            i=0
            for f in fAr:
                fh = os.path.join(source_path,f)
                channel.basic_publish(exchange='',
                                    routing_key=trgt_queue,
                                    body=str(fh))
                i+=1
            print(" [x] Sent", i,"files to the queue")

            connection.close()
    
    except Exception as err:
        print("An error occured while retriving the file.")
        print(str(err))
        traceback.print_tb(err.__traceback__)

if __name__ == '__main__':
    publish()

    consume()