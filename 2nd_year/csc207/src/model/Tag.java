package model;

import java.io.Serializable;

/**
 * A tag, which can be tagged to a photo.
 */
public class Tag implements Serializable {

	/** A serial version UID. */
	private static final long serialVersionUID = 1L;

	/** The prefix of every tag. */
	private static String PREFIX = "@";

	/**
	 * The separator to separate tags from each other when more than one tag
	 * appear in the name of a photo or to separate tags from the original plain
	 * photo name without tags.
	 */
	private static String TAG_SEPARATOR = " ";

	/** A string of content of the tag. */
	private String content;

	/**
	 * A tag, which can be tagged to a photo.
	 *
	 * @param content
	 *            the string of content of a tag without the prefix
	 */
	public Tag(String content) {
		this.content = PREFIX + content;
	}

	/**
	 * Return the PREFIX of a tag.
	 * 
	 * @return the PREFIX
	 */
	public static String getPrefix() {
		return PREFIX;
	}

	/**
	 * Set a string newPrefix to be the new PREFIX.
	 * 
	 * @param newPrefix
	 *            the new prefix to set
	 */
	public static void setPrefix(String newPrefix) {
		PREFIX = newPrefix;
	}

	/**
	 * Return the separator for tags.
	 * 
	 * @return the TAG_SEPARATOR
	 */
	public static String getTagSeparator() {
		return TAG_SEPARATOR;
	}

	/**
	 * Set a string newSeparator to be the new TAG_SEPARATOR.
	 * 
	 * @param newSeparator
	 *            the newSeparator to set
	 */
	public static void setTagSeparator(String newSeparator) {
		TAG_SEPARATOR = newSeparator;
	}

	/**
	 * Return the content of the tag.
	 * 
	 * @return the content
	 */
	public String getContent() {
		return content;
	}

	/**
	 * Return the string representation of a tag.
	 * 
	 * @return the string representation of a tag
	 */
	@Override
	public String toString() {
		return content.toString();
	}

	/**
	 * Return whether item has the same value as this Tag.
	 * 
	 * @return whether item has the same value as this Tag
	 */
	@Override
	public boolean equals(Object item) {
		// Check Type.
		if (item instanceof Tag) {

			// Check instance variable.
			return ((Tag) item).getContent().equals(content);
		} else {

			return false;
		}
	}
}
