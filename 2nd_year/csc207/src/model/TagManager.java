package model;

import java.io.Serializable;
import java.util.ArrayList;

import auxiliary.NotAnExistingTagException;

/**
 * A tag manager, which collects and manages all tags existing in a photo
 * renamer.
 */
public class TagManager implements Serializable {

	/**
	 * The serialVersionUID for TagManager.
	 */
	private static final long serialVersionUID = 1L;

	/**
	 * A list of current existing tags, which is tagged to at least one photo.
	 */
	private ArrayList<Tag> currTags;

	/**
	 * An empty tag manager.
	 */
	public TagManager() {
		currTags = new ArrayList<Tag>();
	}

	/**
	 * A non-empty tag manager.
	 * 
	 * @param allTags
	 *            a list of tags
	 */
	public TagManager(ArrayList<Tag> allTags) {
		currTags = new ArrayList<Tag>();
		for (Tag tag : allTags) {

			// Avoid duplicate tags.
			if (!currTags.contains(tag)) {
				currTags.add(tag);
			}
		}
	}

	/**
	 * Return the set of all tags collected in the TagManger.
	 * 
	 * @return the currTags
	 */
	public ArrayList<Tag> getCurrTags() {
		return currTags;
	}

	/**
	 * Add a new tag to current existing tags of the TagManger. Avoid duplicate.
	 * 
	 * @param newTag
	 *            the new tag to add
	 */
	public void addTag(Tag newTag) {
		if (!currTags.contains(newTag)) {
			currTags.add(newTag);
		}
	}

	/**
	 * Delete a specific tag from existing tags if that tag can be found in the
	 * existing tags of the TagManager.
	 * 
	 * @param unwantedTag
	 *            the tag to delete
	 * @throws NotAnExistingTagException
	 */
	public void deleteTag(Tag unwantedTag) throws NotAnExistingTagException {
		if (!currTags.remove(unwantedTag)) {
			String msg = unwantedTag.toString() + " is not an exisiting tag!";
			throw (new NotAnExistingTagException(msg));
		}
	}
}
