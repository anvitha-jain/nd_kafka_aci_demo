from kafka import KafkaConsumer
from json import loads, dumps, JSONDecodeError

# Configuration
KAFKA_BROKER = '172.31.218.215:9092'  # Replace with your Kafka broker address
KAFKA_TOPIC = 'nd-events'       # Replace with your Kafka topic
KAFKA_GROUP_ID = 'my-group'

# Create Kafka Consumer
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=[KAFKA_BROKER],
    auto_offset_reset='earliest',  # Start reading from beginning if no offset
    enable_auto_commit=False,       # Commit offsets automatically when correct
    group_id=KAFKA_GROUP_ID,
    # value_deserializer=lambda x: loads(x.decode('utf-8'))
)

print(f"Consuming messages from topic '{KAFKA_TOPIC}'. Press Ctrl+C to exit...")
try:
    if consumer:

        for message in consumer:
            # print(f"In for loop {message.value}")
            try:
                json_message=loads(message.value)
                print(f"\nMessage from partition {message.partition}, offset {message.offset}:")
                

                if json_message.get("category")== 'COMPLIANCE':

                # print (message.topic, message.partition, message.offset, message.key)
                # # Pretty print the JSON data
                # print(f"\nMessage keys {message.value.keys()}\n")
                    pretty_json = dumps(json_message, indent=4, sort_keys=True)
                    print(pretty_json)
                
                
                
            except JSONDecodeError:
                print(f"Invalid JSON received: {message.value}")
            except Exception as e:
                print(f"Error processing message: {str(e)}")

except KeyboardInterrupt:
    print("\nConsumption interrupted by user")
except JSONDecodeError:
    print("Invalid JSON message received:")
finally:
    consumer.close()
    print("Kafka consumer closed")
