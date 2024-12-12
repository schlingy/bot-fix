# The following is the code I added to my existing bot to fix the bar issue.
# It seems like atproto suddenly started requiring the aspect ratio to be specified
# for images to be cropped properly. 

from PIL import Image

# find the aspect ratio of the frame 
with Image.open(upload_path) as img:
	width, height = img.size

aspect_ratio = models.AppBskyEmbedDefs.AspectRatio(height=height, width=width)

# ...


# post image to bluesky 
with open(upload_path, 'rb') as f:
    img_data = f.read()
    upload = client.upload_blob(img_data)
    images = [models.AppBskyEmbedImages.Image(alt='episode '+ upload_path[15:18], image=upload.blob, aspect_ratio=aspect_ratio)]
    embed = models.AppBskyEmbedImages.Main(images=images)

    client.com.atproto.repo.create_record(
        models.ComAtprotoRepoCreateRecord.Data(
            repo=client.me.did,
            collection=models.ids.AppBskyFeedPost,
            record=models.AppBskyFeedPost.Record(
                created_at=client.get_current_time_iso(), text='', embed=embed
            ),
        )
    )
