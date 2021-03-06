from collections import namedtuple

image = namedtuple('Image', 'FPS H W C')

def measure_fps(current_time, time_last, n_frames, *args):

    fps = int(float(n_frames) / (current_time - time_last))
    return image(fps, *args), current_time


# def draw_prediction_on_image(
#     image,
#     keypoints_with_scores,
#     crop_region=None,
#     close_figure=False,
#     output_image_height=None,
# ):

#     height, width, channel = image.shape
#     aspect_ratio = float(width) / height
#     fig, ax = plt.subplots(figsize=(12 * aspect_ratio, 12))
#     # To remove the huge white borders
#     fig.tight_layout(pad=0)
#     ax.margins(0)
#     ax.set_yticklabels([])
#     ax.set_xticklabels([])
#     plt.axis("off")

#     im = ax.imshow(image)
#     line_segments = LineCollection([], linewidths=(4), linestyle="solid")
#     ax.add_collection(line_segments)
#     # Turn off tick labels
#     scat = ax.scatter([], [], s=60, color="#FF1493", zorder=3)

#     (keypoint_locs, keypoint_edges, edge_colors) = _keypoints_and_edges_for_display(
#         keypoints_with_scores, height, width
#     )

#     line_segments.set_segments(keypoint_edges)
#     line_segments.set_color(edge_colors)
#     if keypoint_edges.shape[0]:
#         line_segments.set_segments(keypoint_edges)
#         line_segments.set_color(edge_colors)
#     if keypoint_locs.shape[0]:
#         scat.set_offsets(keypoint_locs)

#     if crop_region is not None:
#         xmin = max(crop_region["x_min"] * width, 0.0)
#         ymin = max(crop_region["y_min"] * height, 0.0)
#         rec_width = min(crop_region["x_max"], 0.99) * width - xmin
#         rec_height = min(crop_region["y_max"], 0.99) * height - ymin
#         rect = patches.Rectangle(
#             (xmin, ymin),
#             rec_width,
#             rec_height,
#             linewidth=1,
#             edgecolor="b",
#             facecolor="none",
#         )
#         ax.add_patch(rect)

#     fig.canvas.draw()
#     image_from_plot = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
#     image_from_plot = image_from_plot.reshape(
#         fig.canvas.get_width_height()[::-1] + (3,)
#     )
#     plt.close(fig)
#     if output_image_height is not None:
#         output_image_width = int(output_image_height / height * width)
#         image_from_plot = cv2.resize(
#             image_from_plot,
#             dsize=(output_image_width, output_image_height),
#             interpolation=cv2.INTER_CUBIC,
#         )
#     return image_from_plot
