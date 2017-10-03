package model;

import java.util.ArrayList;

/**
 * A name for a photo, which keeps track of both the string representation of
 * photo name and corresponding tags shown in the string representation of photo
 * name. A valid string representation of a photo name does not start with the
 * prefix of a tag and cannot only contain tags.
 */
public class PhotoName {

	/** The string of the name of a photo. */
	private String strPhotoName;

	/**
	 * The list of all tags in the exact order of their appearance in the name
	 * of a photo.
	 */
	private ArrayList<Tag> lstPhotoTags;

	/**
	 * A PhotoName for a photo, which keeps track of both the string
	 * representation of photo name and corresponding tags shown in the string
	 * representation of photo name.
	 * 
	 * @param photoName
	 *            the string representation of a photo name
	 */
	public PhotoName(String photoName) {
		strPhotoName = photoName;
		lstPhotoTags = extractTags(extractNameWithoutExtension(photoName));
	}

	/**
	 * Return the string representation of the name of a photo.
	 * 
	 * @return the strPhotoName
	 */
	public String getStrPhotoName() {
		return strPhotoName;
	}

	/**
	 * Return a list of all tags in the exact order of their appearance in the
	 * name of a photo.
	 * 
	 * @return the lstPhotoTags
	 */
	public ArrayList<Tag> getLstPhotoTags() {
		return lstPhotoTags;
	}

	/**
	 * Return a string representation of PhotoName.
	 * 
	 * @return the string representation of a PhotoName
	 */
	@Override
	public String toString() {
		return strPhotoName;
	}

	/**
	 * Return whether item has the same value as this PhotoName.
	 * 
	 * @return whether item has the same value as this PhotoName
	 */
	@Override
	public boolean equals(Object item) {
		// Check Type.
		if (item instanceof PhotoName) {

			// Check instance variables.
			return ((PhotoName) item).getLstPhotoTags().equals(lstPhotoTags)
					&& ((PhotoName) item).getStrPhotoName().equals(strPhotoName);
		} else {

			return false;
		}
	}

	/**
	 * Return whether String photoName is a valid string representation of a
	 * name of a photo. A valid string representation of a photo name does not
	 * start with the prefix of a tag and so cannot only contain tags.
	 * 
	 * @param photoName
	 *            the name to check whether is a valid string representation for
	 *            photo name
	 * @return whether photoName is a valid string representation of a name of a
	 *         photo
	 */
	public static boolean isValidStrPhotoName(String photoName) {
		return !photoName.startsWith(Tag.getPrefix());
	}

	/**
	 * Extract the string representation of a photo name without extension from
	 * photoName. Precondition: photoName is a valid string representation of a
	 * photo name, i.e. it does not start with prefix of a tag and does not only
	 * contain tags.
	 * 
	 * @param photoName
	 *            the photo name to extract the part of the name without the
	 *            extension
	 * @return the string representation of a photo name without extension
	 */
	public static String extractNameWithoutExtension(String photoName) {
		int index = photoName.lastIndexOf(".");
		return photoName.substring(0, index);
	}

	/**
	 * Extract the string representation of the extension (including the "." as
	 * a separator) from photoName. Precondition: photoName is a valid string
	 * representation of a photo name, i.e. it does not start with prefix of a
	 * tag and does not only contain tags.
	 * 
	 * @param photoName
	 *            the photo name to extract the extension
	 * @return the string representation of the extension (including the "." as
	 *         a separator) from photoName
	 */
	public static String extractExtension(String photoName) {
		int index = photoName.lastIndexOf(".");
		return photoName.substring(index);
	}

	/**
	 * Get the plain name, i.e. without tags, from a given string representation
	 * of a name of a photo, which possibly contains tags. Precondition:
	 * photoName is a valid string representation of a photo name, i.e. it does
	 * not start with prefix of a tag and does not only contain tags.
	 * 
	 * @param photoName
	 *            the photo name string, which possibly contains tags, to
	 *            extract plain photo name without tags
	 * @return the string of photo name without tags
	 */
	public static String extractPlainNameWithoutTags(String photoName) {
		// Use tag separator and tag prefix to get the beginning part of the
		// photoName, which is before the first tag if here's any tag;
		// otherwise photoName is already a plain photo name without tags.
		int index = photoName.indexOf(Tag.getTagSeparator() + Tag.getPrefix());
		return (index == -1) ? photoName : photoName.substring(0, index);
	}

	/**
	 * Extract a list of all tags in photoNameWithoutExtension, in consistent
	 * with the order of their appearance in photoNameWithoutExtension.
	 * Precondition: photoNameWithoutExtension is a valid string representation
	 * of a photo name without extension, i.e. it does not start with prefix of
	 * a tag and does not only contain tags and does not contain the extension.
	 * 
	 * @param photoNameWithoutExtension
	 *            the photo name without extension to extract tags
	 * @return a list of all tags in photoName
	 */
	public static ArrayList<Tag> extractTags(String photoNameWithoutExtension) {
		// Construct an accumulator.
		ArrayList<Tag> acc = new ArrayList<Tag>();

		// Split the string photoName based on separator and prefix for tags
		String[] temp = photoNameWithoutExtension.split(Tag.getTagSeparator() + Tag.getPrefix());
		int bound = temp.length;

		// When photoName does have any tags.
		if (bound >= 2) {

			// Since photoName is a valid string representation of a photo
			// name, then the splitting result has its first item to be a
			// plain photo name without tags; we don't add that into the
			// accumulator.
			for (int i = 1; i < bound; i++) {

				// Instantiate a Tag object to be added to the accumulator
				Tag tag = new Tag(temp[i]);
				acc.add(tag);
			}
		}
		return acc;
	}

	/**
	 * Return a string representation for the tail of a name of a photo by
	 * putting all tags together in order, which is in consistent with the order
	 * of their appearance in the corresponding list collecting them.
	 * 
	 * @param tags
	 *            a list of all tags to be joined to get a string representation
	 *            for the tail of a name of a photo
	 * @return a string representation for the tail of a name of a photo
	 *         containing only string representation of tags and the string
	 *         begins with a tag separator
	 */
	public static String combineTags(ArrayList<Tag> tags) {
		// Construct an accumulator.
		String result = "";

		// Loop over list of tags and generate string representation.
		for (Tag t : tags) {
			result += Tag.getTagSeparator() + t.toString();
		}

		return result;
	}
}
