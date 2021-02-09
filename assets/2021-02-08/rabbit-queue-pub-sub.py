import os
import pika
import traceback
import sys

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
    return


def consume ():
    rbt_srv = 'rabbit-queue'
    src_queue = 'new_files'
    try:
        print(' [-] Connecting to RabbitMQ server',rbt_srv)
        with pika.BlockingConnection(pika.ConnectionParameters(rbt_srv)) as connection:
            channel = connection.channel()

            print(' [+] Connected to RabbitMQ')
            # Declare source queue
            channel.queue_declare(queue=src_queue, durable=True)

            def callback(ch, method, properties, filePath):
                print(" [*] Retrieved file path {0}".format(filePath))
                # Ack to the queue message has been recieved successfuly
                ch.basic_ack(delivery_tag=method.delivery_tag)
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue=src_queue, on_message_callback=callback, auto_ack=False)

            print(' [*] Waiting for messages. To exit press CTRL+C')
            channel.start_consuming()

            connection.close()
    except Exception as err:
        print()
        print("An error occured wwhile retriving the file.")
        print(str(err))
        traceback.print_tb(err.__traceback__)
    return


if __name__ == '__main__':
    try:
        publish()
        consume()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)