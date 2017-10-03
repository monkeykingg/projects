package model;

import java.awt.image.BufferedImage;
import javax.imageio.ImageIO;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Date;
import javafx.util.Pair;

import auxiliary.FailToRenamePhotoFileException;
import auxiliary.FileTypeException;

/**
 * A photo ranamer, which mainly manages the name of photos based on a set of
 * tags.
 */
public class PhotoRenamer {

	/**
	 * Two modes for renaming photos. "D" is for deleting tags of one photo. "A"
	 * is for adding tags on one photo.
	 */
	private static char[] renameMode = { 'D', 'A' };

	/** The string representation for the notation that a listing is over. */
	private static String endListingNotation = "-----------" + "List Over" + "-----------";

	/**
	 * A cabinet of photos and directories, which shows the hierarchy of
	 * directory system for photos rooted at one specified root.
	 */
	private PhotoManager photoCabinet;

	/** The path representing a directory to put configuration files. */
	private String configPath;

	/**
	 * A photo renamer, which can be constructed based on either a directory or
	 * a single photo.
	 * 
	 * @param root
	 *            The root of the directory tree on which a photo renamer is
	 *            constructed. The root can be either a directory or a single
	 *            photo.
	 * @param rootNode
	 *            The FileNode representing the root of the directory tree on
	 *            which a photo renamer is constructed. The rootNode can either
	 *            represent a directory or a single photo.
	 * @throws FileTypeException
	 */
	public PhotoRenamer(File root, FileNode rootNode) throws FileTypeException {
		// Initialize photoCabinet.
		photoCabinet = new PhotoManager(root, rootNode);

		// Check type of the root this PhotoRenamer is based on.
		// Initialize configPath.
		if (root.isDirectory()) {

			// If root is a directory, put configuration file in root.
			configPath = root.getAbsolutePath();
		} else if (rootNode.isPhoto()) {

			// If root is a photo, put configuration file in its parent
			// directory.
			configPath = root.getParentFile().getAbsolutePath();
		} else {

			String msg = root.getName()
					+ " is neither a directory nor a photo, can't construct a PhotoRenamer on that!";
			throw new FileTypeException(msg);
		}
	}

	/**
	 * Return the cabinet of photos and directories, which shows the hierarchy
	 * of directory system for photos rooted at one specified root.
	 * 
	 * @return the photoCabinet
	 */
	public PhotoManager getPhotoCabinet() {
		return photoCabinet;
	}

	/**
	 * Return all valid choices for rename mode.
	 * 
	 * @return the rename modes
	 */
	public static char[] getRenameMode() {
		return renameMode;
	}

	/**
	 * Return the string representation for the notation that a listing is over.
	 * 
	 * @return the endListingNotation
	 */
	public static String getEndListingNotation() {
		return endListingNotation;
	}

	/**
	 * Set the string representation for the notation that a listing is over to
	 * be a new string endListingNotation.
	 * 
	 * @param endListingNotation
	 *            the endListingNotation to set
	 */
	public static void setEndListingNotation(String endListingNotation) {
		PhotoRenamer.endListingNotation = endListingNotation;
	}

	/**
	 * Return whether a candidate string represents a valid rename mode.
	 * 
	 * @param candidate
	 *            the string to be checked whether is a valid rename mode
	 * @return whether the candidate string represents a valid rename mode
	 */
	public boolean isValidMode(String candidate) {
		return candidate.equals(renameMode[0]) || candidate.equals(renameMode[1]);
	}

	/**
	 * Return a string buffer representation of the contents of the tree rooted
	 * at photoTree in fileCabinet (only taking directories and photos into
	 * account), prepending each file name with prefix, and adding and
	 * additional FileManager.FILE_PREFIX for subdirectory contents.
	 * 
	 * @return a string buffer representation of the contents of the tree rooted
	 *         at photoTree in fileCabinet (only taking directories and photos
	 *         into account)
	 */
	public StringBuffer printPhotoTree() {
		StringBuffer photoTreeString = new StringBuffer();
		FileManager.buildDirectoryContents(photoCabinet.getPhotoTree(), photoTreeString, "");
		return photoTreeString;
	}

	/**
	 * Return a string buffer representation of the contents of the tree rooted
	 * at rootNode in fileCabinet, prepending each file name with prefix, and
	 * adding and additional FileManager.FILE_PREFIX for subdirectory contents.
	 * 
	 * @return a string buffer representation of the contents of the tree rooted
	 *         at photoTree in fileCabinet
	 */
	public StringBuffer printEntireTree() {
		StringBuffer entireTreeString = new StringBuffer();
		FileManager.buildDirectoryContents(photoCabinet.getRootNode(), entireTreeString, "");
		return entireTreeString;
	}

	/**
	 * Return a string buffer representation listing all tags existing in this
	 * PhotoRenamer.
	 * 
	 * @return a string buffer representation listing all tags existing in this
	 *         PhotoRenamer
	 */
	public StringBuffer listTags() {
		StringBuffer allTags = new StringBuffer();
		allTags.append("All existing tags are listed as the following: \n");

		// Collect string representation for all tags in the PhotoRenamer
		ArrayList<Tag> tagLst = photoCabinet.getExistingTags().getCurrTags();
		for (Tag tag : tagLst) {
			allTags.append(tag.toString() + "\n");
		}
		allTags.append(endListingNotation);
		return allTags;
	}

	/**
	 * Return a string buffer representation listing all photos existing in this
	 * PhotoRenamer.
	 * 
	 * @return a string buffer representation listing all photos existing in
	 *         this PhotoRenamer
	 */
	public StringBuffer listPhotos() {
		StringBuffer allPhotos = new StringBuffer();
		allPhotos.append("All existing photos are listed as the following: \n");

		// Collect string representation for all photos in the PhotoRenamer
		ArrayList<Pair<File, PhotoNode>> photoLst = photoCabinet.getFlattenedPhotoCollection();
		for (Pair<File, PhotoNode> photoPair : photoLst) {
			allPhotos.append(photoPair.getKey().getName() + "\n");
		}
		allPhotos.append(endListingNotation);
		return allPhotos;
	}

	/**
	 * Return a 2-element pair for (photo File, corresponding PhotoNode)
	 * representing the photo file want to choose at the specified path if
	 * possible.
	 * 
	 * @param path
	 *            the absolute path for the photo you want to choose
	 * @return a 2-element pair for (photo File, corresponding PhotoNode)
	 *         representing the photo file want to choose at the specified path
	 * @throws FileNotFoundException
	 */
	public Pair<File, PhotoNode> choosePhoto(String absPath) throws FileNotFoundException {
		Pair<File, PhotoNode> result = null;
		File aimPhoto = new File(absPath);

		// Check whether we do have a photo in the specified path.
		// If it is not even a photo, we don't bother to do anything else.
		BufferedImage img = null;
		try {
			img = ImageIO.read(aimPhoto);
		} catch (IOException e) {
			e.printStackTrace();
		}

		// When we do have a photo in the specified path, we check whether that
		// photo is in our PhotoRenamer.
		if (img != null) {
			for (Pair<File, PhotoNode> photoPair : photoCabinet.getFlattenedPhotoCollection()) {

				// Try to find a pair in the collection, which matches the photo
				// in the specified path
				if (photoPair.getKey().getAbsolutePath().equals(absPath)) {
					result = photoPair;
				}
			}

			// If we can't find a matching pair for the photo in the specified
			// path in the flattenedPhotoCollection, throw an exception.
			if (result == null) {
				String msg = aimPhoto.getName() + " is not an existing photo in this PhotoRenamer!";
				throw new FileNotFoundException(msg);
			}
		}

		// When an exception was not thrown and result is not null, we do find a
		// matching pair and we can choose the photo we want.
		return result;
	}

	/**
	 * Return a string buffer representation reporting the process of adding or
	 * removing a specified tag for all photos by specifying those photos whose
	 * name was not changed. Rename all photos by deleting a tag or adding a tag
	 * to all photos. Precondition: mode is a valid renaming mode, i.e. either
	 * 'D' or 'A'
	 * 
	 * @param tag
	 *            the tag to add or delete
	 * @param mode
	 *            the mode of renaming, either 'D' for deleting a tag or 'A' for
	 *            adding a tag
	 * @return a string buffer representation reporting the process of adding or
	 *         removing a specified tag for all photos by specifying those
	 *         photos whose name was not changed
	 * @throws IOException
	 */
	public StringBuffer renameAll(Tag tag, char mode) throws IOException {
		StringBuffer result = new StringBuffer();

		// Loop over all photos
		ArrayList<Pair<File, PhotoNode>> flattenedPhotos = photoCabinet.getFlattenedPhotoCollection();
		for (Pair<File, PhotoNode> photoPair : flattenedPhotos) {

			if (mode == renameMode[1]) {

				// Add a tag for all photos.
				// If failed, report in the result.
				try {
					photoCabinet.logTagPhoto(photoPair.getKey(), photoPair.getValue(), tag);
				} catch (FailToRenamePhotoFileException e) {
					result.append(photoPair.getValue().getName() + "\n");
				}
			} else if (mode == renameMode[0]) {

				// Remove a tag for all photos.
				// If failed, report in the result.
				try {
					photoCabinet.logDetagPhoto(photoPair.getKey(), photoPair.getValue(), tag);
				} catch (FailToRenamePhotoFileException e) {
					result.append(photoPair.getValue().getName() + "\n");
				}
			}
		}

		// Rewrite TagManager after updating that.
		photoCabinet.writeTagManger(photoCabinet.getExistingTags(), configPath + File.separator + "Tags.ser");

		// Return result as a report.
		String s1;
		String s2;
		if (mode == renameMode[1]) {
			s1 = "Add";
			s2 = "add";
		} else {
			s1 = "Remove";
			s2 = "remove";
		}
		if (result.length() == 0) {
			result.append(s1 + " the tag, " + tag.toString() + ". to all photos.");
		} else {
			result.insert(0,
					"Photos failed to " + s2 + " the tag, " + tag.toString() + ", are listed as the following: \n");
		}
		return result;
	}

	/**
	 * Return a string buffer representation reporting the process of adding or
	 * removing a list of tags for all photos by specifying those photos whose
	 * name was not changed. Rename all photos by deleting a list of tags or
	 * adding a list of tags to all photos.
	 * 
	 * @param tag
	 *            a list of tags to add or delete
	 * @param mode
	 *            the mode of renaming, either 'D' for deleting or 'A' for
	 *            adding
	 * @return a string buffer representation reporting the process of adding or
	 *         removing a list of tags for all photos by specifying those photos
	 *         whose name was not changed
	 * @throws IOException
	 */
	public StringBuffer renameAllByCollection(ArrayList<Tag> tags, char mode) throws IOException {
		StringBuffer result = new StringBuffer();

		// Loop over all photos
		ArrayList<Pair<File, PhotoNode>> flattenedPhotos = photoCabinet.getFlattenedPhotoCollection();
		for (Pair<File, PhotoNode> photoPair : flattenedPhotos) {

			if (mode == renameMode[1]) {

				// Add a list of tags for all photos.
				// If failed, report in the result.
				try {
					photoCabinet.logTagPhotoByCollection(photoPair.getKey(), photoPair.getValue(), tags);
				} catch (FailToRenamePhotoFileException e) {
					result.append(photoPair.getValue().getName() + "\n");
				}
			} else if (mode == renameMode[0]) {

				// Remove a list of tags for all photos.
				// If failed, report in the result.
				try {
					photoCabinet.logDetagPhotoByCollection(photoPair.getKey(), photoPair.getValue(), tags);
				} catch (FailToRenamePhotoFileException e) {
					result.append(photoPair.getValue().getName() + "\n");
				}
			}
		}

		// Rewrite TagManager after updating that.
		photoCabinet.writeTagManger(photoCabinet.getExistingTags(), configPath + File.separator + "Tags.ser");

		// Return result as a report.
		String s1;
		String s2;
		if (mode == renameMode[1]) {
			s1 = "Add";
			s2 = "add";
		} else {
			s1 = "Remove";
			s2 = "remove";
		}
		if (result.length() == 0) {
			result.append(s1 + " a list of tags to all photos.");
		} else {
			result.insert(0, "Photos failed to " + s2 + " a list of tags are listed as the following: \n");
		}
		return result;
	}

	/**
	 * Rename a single photo by deleting a tag or adding a tag.
	 * 
	 * @param photo
	 *            the File photo to rename
	 * @param photoNode
	 *            the corresponding PhotoNode to rename
	 * @param tag
	 *            the tag to add or delete
	 * @param mode
	 *            the mode of renaming, either 'D' for deleting a tag or 'A' for
	 *            adding a tag
	 * @throws FailToRenamePhotoFileException
	 * @throws IOException
	 */
	public void rename(File photo, PhotoNode photoNode, Tag tag, char mode)
			throws FailToRenamePhotoFileException, IOException {
		if (mode == renameMode[1]) {

			// Add a tag.
			photoCabinet.logTagPhoto(photo, photoNode, tag);
		} else if (mode == renameMode[0]) {

			// Remove a tag.
			photoCabinet.logDetagPhoto(photo, photoNode, tag);
		}

		// Rewrite TagManager after updating that.
		photoCabinet.writeTagManger(photoCabinet.getExistingTags(), configPath + File.separator + "Tags.ser");
	}

	/**
	 * Rename a single photo by deleting a list of tags or adding a list of
	 * tags.
	 * 
	 * @param photo
	 *            the File photo to rename
	 * @param photoNode
	 *            the corresponding PhotoNode to rename
	 * @param tag
	 *            the tag to add or delete
	 * @param mode
	 *            the mode of renaming, either 'D' for deleting a tag or 'A' for
	 *            adding a tag
	 * @throws FailToRenamePhotoFileException
	 * @throws IOException
	 */
	public void renameByCollection(File photo, PhotoNode photoNode, ArrayList<Tag> tags, char mode)
			throws FailToRenamePhotoFileException, IOException {
		if (mode == renameMode[1]) {

			// Add a list of tags.
			photoCabinet.logTagPhotoByCollection(photo, photoNode, tags);
		} else if (mode == renameMode[0]) {

			// Remove a list of tags.
			photoCabinet.logDetagPhotoByCollection(photo, photoNode, tags);
		}

		// Rewrite TagManager after updating that.
		photoCabinet.writeTagManger(photoCabinet.getExistingTags(), configPath + File.separator + "Tags.ser");
	}

	/**
	 * Return a string buffer representation reporting the process of undoing
	 * name for all photos by specifying those photos whose name was not
	 * changed. Undo the name of all photos in this PhotoRenamer back to the
	 * latest name before current name if there exists a past name.
	 * 
	 * @return a string buffer representation reporting the process of undoing
	 *         name for all photos by specifying those photos whose name was not
	 *         changed
	 * @throws IOException
	 */
	public StringBuffer undoNameAll() throws IOException {
		StringBuffer result = new StringBuffer();
		ArrayList<Pair<File, PhotoNode>> flattenedPhotos = photoCabinet.getFlattenedPhotoCollection();

		// Loop over all photos.
		for (Pair<File, PhotoNode> photoPair : flattenedPhotos) {
			try {

				// Undo the name.
				photoCabinet.logUndoName(photoPair.getKey(), photoPair.getValue());
			} catch (FailToRenamePhotoFileException e) {

				// If can't undo the name for one photo, record that in the
				// StringBuffer result.
				result.append(photoPair.getValue().getName() + "\n");
			}
		}

		// Rewrite TagManager after updating that.
		photoCabinet.writeTagManger(photoCabinet.getExistingTags(), configPath + File.separator + "Tags.ser");

		// Return result as a report.
		if (result.length() == 0) {
			result.append("Undo all photo names.");
		} else {
			result.insert(0, "Photos failed to undo their names are listed below: \n");
		}
		return result;
	}

	/**
	 * Undo the name of a photo back to the latest name before current name if
	 * there exists a past name.
	 * 
	 * @param photo
	 *            the File photo to undo its name
	 * @param photoNode
	 *            the corresponding PhotoNode to undo its name
	 * @throws IOException
	 * @throws FailToRenamePhotoFileException
	 * 
	 */
	public void undoName(File photo, PhotoNode photoNode) throws IOException, FailToRenamePhotoFileException {
		// Undo the name.
		photoCabinet.logUndoName(photo, photoNode);

		// Rewrite TagManager after updating that.
		photoCabinet.writeTagManger(photoCabinet.getExistingTags(), configPath + File.separator + "Tags.ser");
	}

	/**
	 * Revert the name of a photo back to a specified oldName if oldName is an
	 * existing past name for the photo. If there were several oldName existing
	 * as past names, revert to the latest one.
	 * 
	 * 
	 * @param photo
	 *            the File photo to revert its name back to oldName
	 * @param photoNode
	 *            the corresponding PhotoNode to revert its name back to oldName
	 * @param oldName
	 *            the specified oldName to revert back to if it is an existing
	 *            past name
	 * @throws IOException
	 * @throws FailToRenamePhotoFileException
	 */
	public void revertName(File photo, PhotoNode photoNode, PhotoName oldName)
			throws IOException, FailToRenamePhotoFileException {
		// Revert the name.
		photoCabinet.logRevertName(photo, photoNode, oldName);

		// Rewrite TagManager after updating that.
		photoCabinet.writeTagManger(photoCabinet.getExistingTags(), configPath + File.separator + "Tags.ser");
	}

	/**
	 * Revert the name of the photo back to the closest state merely before a
	 * particular time date if there were past names existed before that date
	 * for the photo. If the first name for the photo was generated after that
	 * date, revert back to the first name of the photo.
	 * 
	 * @param photo
	 *            the File photo to revert its name back
	 * @param photoNode
	 *            the corresponding PhotoNode to revert its name back
	 * @param date
	 *            the time to revert back to
	 * @throws IOException
	 */
	public void revertNameByDate(File photo, PhotoNode photoNode, Date date) throws IOException {
		// Revert the name by date.
		photoCabinet.logRevertNameByDate(photo, photoNode, date);

		// Rewrite TagManager after updating that.
		photoCabinet.writeTagManger(photoCabinet.getExistingTags(), configPath + File.separator + "Tags.ser");
	}

	/**
	 * Return a string buffer representation reporting the process of reverting
	 * the name of all photos in the PhotoRenamer back to the closest state
	 * merely before a particular time date if there were past names existed
	 * before that date for the photo. If the first name for one photo was
	 * generated after that date, revert back to the first name of the photo.
	 * 
	 * @param date
	 *            the time to revert back to
	 * @return a string buffer representation reporting the process of reverting
	 *         the name of all photos in the PhotoRenamer back to the closest
	 *         state merely before a particular time date
	 * @throws IOException
	 */
	public StringBuffer revertAllNameByDate(Date date) throws IOException {
		StringBuffer result = new StringBuffer();
		ArrayList<Pair<File, PhotoNode>> flattenedPhotos = photoCabinet.getFlattenedPhotoCollection();

		// Revert the name by date for all photos in the PhotoRenamer.
		for (Pair<File, PhotoNode> photoPair : flattenedPhotos) {
			photoCabinet.logRevertNameByDate(photoPair.getKey(), photoPair.getValue(), date);
		}

		// Rewrite TagManager after updating that.
		photoCabinet.writeTagManger(photoCabinet.getExistingTags(), configPath + File.separator + "Tags.ser");

		// Return result as a report.
		if (result.length() == 0) {
			result.append("Revert all photo names back to the state merely before " + date.toString());
		} else {
			result.insert(0,
					"Photos failed to revert their names back to the state merely before " + date.toString() + ": \n");
		}
		return result;
	}

	/**
	 * Return a string buffer representation listing names of all photos
	 * containing a specific tag aimTag.
	 * 
	 * @param aimTag
	 *            the specific tag for search
	 * @return a string buffer representation listing names of all photos
	 *         containing a specific tag aimTag
	 */
	public StringBuffer printTagSearch(Tag aimTag) {
		StringBuffer result = new StringBuffer();
		ArrayList<Pair<File, PhotoNode>> photoPairLst = photoCabinet
				.searchTag(photoCabinet.getFlattenedPhotoCollection(), aimTag);

		if (photoPairLst.isEmpty()) {

			// No photo has aimTag in the name.
			result.append("No photo has tag: " + aimTag.toString());
		} else {

			// Do find at least one photo having aimTag in the name.
			result.append("List photo(s) containing tag, " + aimTag.toString() + ", as the following: \n");
			for (Pair<File, PhotoNode> photoPair : photoPairLst) {
				result.append(photoPair.getValue().getName() + "\n");
			}
			result.append(endListingNotation);
		}

		return result;
	}
}
